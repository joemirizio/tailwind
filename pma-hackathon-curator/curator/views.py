from django.shortcuts import render
from django.db import connection
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

import json
import random
import re
from .models import Artwork, Gallery, GalleryActivity, Persona, Reaction, ReactionType, Visitor

def get_personas(request):
  return _json_serialize(Persona.objects.all())

def get_reactions(request):
  return _json_serialize(ReactionType.objects.all())

def get_galleries(request):
  return _json_serialize(Gallery.objects.all())

def get_gallery_activity(request, gallery_id):
  persona_id = request.GET.get('persona_id')
  if not persona_id:
    raise TypeError('Invalid persona_id')
  activities = GalleryActivity.objects.filter(gallery_id=gallery_id, persona__id=persona_id)
  if activities.exists():
    activity = activities.get()
  else:
    persona_name = Persona.objects.get(pk=persona_id).name
    gallery_name = Gallery.objects.get(pk=gallery_id).name
    raise ValueError('No activities found for {} in {}'.format(persona_name, gallery_name))
  return _json_serialize((activity,))

def get_gallery_recommendation(request, gallery_id):
  visitor_id = request.GET.get('visitor_id')
  if not visitor_id:
    raise TypeError('Invalid visitor_id')
  
  visitor = Visitor.objects.get(pk=visitor_id)
  persona = visitor.persona

  NO_RESPONSE = 0

  persona_reactions = (Reaction.objects
                       .filter(visitor__persona=persona, artwork__gallery=gallery_id)
                       .values('reaction_type__value', 'artwork')
                       .annotate(weight=Sum('reaction_type__value'))
                       .distinct().order_by('-weight'))

  visitor_reactions = visitor.reaction_set.filter(artwork__gallery=gallery_id)
  
  reason = ''
  if visitor_reactions.filter(reaction_type__value__gt=0).exists():
    try:
      recommendations = recommendations_visitor(visitor_id, gallery_id)
      artwork = recommendations[0]['artwork']
      reason = recommendations[0]['description']
    except:
      raise Http404("No more personal recommendations")
  else:
    # For gallery, no visitor reactions, so choose based on persona reactions
    visitor_reactions_ids = [reaction.artwork.id for reaction in visitor_reactions]
    filtered_reactions = [reaction['artwork']
                          for reaction in persona_reactions if reaction['artwork'] not in visitor_reactions_ids]
    if not filtered_reactions:
      raise Http404("No more persona recommendations")
    artwork = Artwork.objects.get(pk=filtered_reactions[0])
    reason = 'Highly rated amongst {}s. React positively to this piece to see more like this one!'.format(persona.name)

  # Add a "no response" default reaction
  react(visitor_id, NO_RESPONSE, artwork.id)

  # Serialize singular artwork
  artwork_serialized = serializers.serialize('json', (artwork,))
  artwork_serialized_dict = json.loads(artwork_serialized)
  artwork = artwork_serialized_dict[0]

  # Wrap response and reason
  response = { 'recommendation': artwork, 'reason': reason }
  return _dict_serialize(response)

@csrf_exempt
def add_reaction(request):
  if request.method != 'POST':
    raise TypeError('Only POST is supported')

  visitor_id = request.POST.get('visitor_id')
  reaction_type_id = request.POST.get('reaction_type_id')
  artwork_id = request.POST.get('artwork_id')
  if visitor_id is None:
    raise TypeError('Invalid visitor_id')
  if reaction_type_id is None:
    raise TypeError('Invalid reaction_type_id')
  if artwork_id is None:
    raise TypeError('Invalid artwork_id')

  try:
    react(visitor_id, reaction_type_id, artwork_id)
    return _dict_serialize({ 'message': 'ok' })
  except ObjectDoesNotExist:
    return _dict_serialize({ 'error': 'Object does not exist' })

@csrf_exempt
def add_visitor(request):
  if request.method != 'POST':
    raise TypeError('Only POST is supported')

  visitor_id = request.POST.get('visitor_id')
  persona_id = request.POST.get('persona_id')
  if visitor_id is None:
    raise TypeError('Invalid visitor_id')
  if persona_id is None:
    raise TypeError('Invalid persona_id')

  try:
    persona = Persona.objects.get(pk=persona_id)
    Visitor(id=visitor_id, persona=persona).save()
    return _dict_serialize({ 'message': 'ok' })
  except ObjectDoesNotExist:
    return _dict_serialize({ 'error': 'Object does not exist' })


def _json_serialize(objects):
  data = serializers.serialize('json', objects)
  return HttpResponse(data, content_type="application/json")

def _dict_serialize(_dict):
  return HttpResponse(json.dumps(_dict), content_type="application/json")


def index(request):
  return HttpResponseRedirect("http://museumcrawlers.com:8080")
  #return render(request, 'index.html')


def recommendations_visitor(visitor_id, gallery_id):
  with connection.cursor() as cursor:
    cursor.execute('''
      SELECT 
        B.artwork_id, 
        group_concat(replace(B.key, '|', '.'), '|') AS reason, 
        group_concat(replace(B.value, '|', '.'), '|') AS rationale, 
        SUM(B.weight + REACTIONS.score) AS weight
      FROM (
        SELECT * FROM curator_artworkattribute ORDER BY weight DESC
      ) AS B
      JOIN (
        SELECT SUM(RT.value * A.weight) AS score, A.key, A.value
        FROM curator_artworkattribute A
        JOIN curator_reaction R ON A.artwork_id = R.artwork_id
        JOIN curator_reactiontype RT ON R.reaction_type_id = RT.id
        JOIN curator_artwork ART ON R.artwork_id = ART.id
        WHERE R.visitor_id = %s AND RT.value > 0
        GROUP BY A.key, A.value
        ORDER BY score DESC
      ) AS REACTIONS ON 
          REACTIONS.key = B.key AND
          REACTIONS.value = B.value
      WHERE
        B.artwork_id NOT in (
          SELECT R.artwork_id
          FROM curator_reaction R 
          JOIN curator_reactiontype RT ON R.reaction_type_id = RT.id
          JOIN curator_artwork ART ON R.artwork_id = ART.id
          WHERE R.visitor_id = %s AND ART.gallery_id = %s
        )
      GROUP BY B.artwork_id
      ORDER BY weight DESC;
    ''', [str(visitor_id), str(visitor_id), str(gallery_id)])
    rows = cursor.fetchall()

  rows = [row_append(row, recommendation_descriptions(row)) for row in rows]
  recommendations = [dict(weight=row[3], description=row[4], artwork=Artwork.objects.get(pk=row[0])) for row in rows]
  context = {'recommendations': recommendations}
  return recommendations

  #return render(request, 'recommendations.html', context=context)

def row_append(row, value):
  ret = list(row)
  ret.append(value)
  return ret

def react(visitor_id, reaction_type_id, artwork_id):
  previous_reaction = Reaction.objects.filter(visitor_id=visitor_id, artwork_id=artwork_id)
  reaction = ReactionType.objects.get(pk=reaction_type_id)
  if previous_reaction.exists():
    previous_reaction = previous_reaction.get()
    previous_reaction.reaction_type = reaction
    previous_reaction.save()
  else:
    visitor = Visitor.objects.get(pk=visitor_id)
    artwork = Artwork.objects.get(pk=artwork_id)
    reaction = Reaction(visitor=visitor, reaction_type=reaction, artwork=artwork).save()
  return reaction

def recommendation_descriptions(recommendation):
  reasons = recommendation[1].split('|')
  rationales = recommendation[2].split('|')
  messages = []

  for i, reason in enumerate(reasons):
    rationale = rationales[i]
    rationaleLowerCase = rationale.lower()

    if reason == 'GalleryShort':
      messages.append('located in this gallery')
    if reason == 'Wing':
      if not 'GalleryShort' in reasons:
        messages.append('located in this wing')
    if reason == 'Classification':
      # TODO Add appropriate pluralization
      messages.append('{}'.format(rationaleLowerCase))
    if reason == 'Style':
      messages.append('in the {} style'.format(rationaleLowerCase))
    if reason == 'Movement':
      messages.append('in the {} movement'.format(rationale))
    if reason == 'SocialTags':
      messages.append('have to do with {}'.format(rationale))
    
  # Add 'and'
  message_length = len(messages)
  if message_length > 1:
    messages[message_length - 1] = 'and ' + messages[message_length - 1]

  message = ', '.join(messages) if (message_length > 2) else ' '.join(messages)
  return 'You like pieces that are ' + message;
