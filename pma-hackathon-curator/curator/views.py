from django.shortcuts import render
from django.db import connection
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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
  if activities:
    activity = activities[0]
  else:
    persona_name = Persona.objects.get(pk=persona_id).name
    gallery_name = Gallery.objects.get(pk=gallery_id).name
    raise ValueError('No activities found for {} in {}'.format(persona_name, gallery_name))
  return _json_serialize((activity,))

def get_gallery_recommendation(request, gallery_id):
  persona_id = request.GET.get('persona_id')
  if not persona_id:
    raise TypeError('Invalid persona_id')
  # TODO implement
  artwork = random.choice(Artwork.objects.filter(gallery_id=gallery_id))
  return _json_serialize((artwork,))

@csrf_exempt
def add_reaction(request, visitor_id, reaction_type_id, artwork_id):
  visitor = Visitor.objects.get(pk=visitor_id)
  reaction = ReactionType.objects.get(pk=reaction_type_id)
  artwork = Artwork.objects.get(pk=artwork_id)
  Reaction(visitor=visitor, reaction_type=reaction, artwork=artwork).save()
  return _dict_serialize({ 'message': 'ok'})

@csrf_exempt
def add_visitor(request):
  visitor_id = request.POST.get('vistor_id')
  persona_id = request.POST.get('persona_id')
  if not visitor_id:
    raise TypeError('Invalid id')
  if not persona_id:
    raise TypeError('Invalid persona')
  persona = Persona.objects.get(pk=persona_id)
  Visitor(id=visitor_id, persona=persona).save()
  return _dict_serialize({ 'message': 'ok'})

def _json_serialize(objects):
  data = serializers.serialize('json', objects)
  return HttpResponse(data, content_type="application/json")

def _dict_serialize(_dict):
  return HttpResponse(json.dumps(_dict), content_type="application/json")


def recommendation(request):
  return HttpResponseRedirect("http://museumcrawlers.com:8080")
  #return render(request, 'index.html')

def recommendation_for_gallery(request, gallery_id, persona=None):
  objects = Artwork.objects.filter(gallery_id=gallery_id)
  data = serializers.serialize('json', objects)
  return HttpResponse(data, content_type="application/json")

def recommendations_for_artwork(request, artwork_id, persona=None):
  with connection.cursor() as cursor:
    cursor.execute('''
      SELECT 
        B.artwork_id, 
        group_concat(replace(B.key, '|', '.'), '|') as reason, 
        group_concat(replace(B.value, '|', '.'), '|') as rationale, 
        SUM(B.weight) as weight
      FROM (
        SELECT * FROM curator_artworkattribute ORDER BY weight DESC
      ) A
      JOIN (
        SELECT * FROM curator_artworkattribute ORDER BY weight DESC
      ) B ON A.key = B.key
      WHERE
        A.artwork_id = %s AND 
        A.value = B.value AND
        B.artwork_id != A.artwork_id
      GROUP BY B.artwork_id
      ORDER BY weight DESC;
    ''', [str(artwork_id)])
    rows = cursor.fetchall()

  rows = [row_append(row, recommendation_descriptions(row)) for row in rows]
  recommendations = [dict(weight=row[3], description=row[4], artwork=Artwork.objects.get(pk=row[0])) for row in rows]
  context = {'recommendations': recommendations}

  return render(request, 'recommendations.html', context=context)

def row_append(row, value):
  ret = list(row)
  ret.append(value)
  return ret

def recommendation_descriptions(recommendation):
  reasons = recommendation[1].split('|')
  rationales = recommendation[2].split('|')
  messages = []

  for i, reason in enumerate(reasons):
    rationale = rationales[i]
    rationaleLowerCase = rationale.lower()
    rationalePlural = '' if re.match(r's$', rationaleLowerCase) else 's'

    if reason == 'GalleryShort':
      messages.append('located in the same gallery')
    if reason == 'Wing':
      if not 'GalleryShort' in reasons:
        messages.append('located in the same wing')
    if reason == 'Classification':
      # TODO Add appropriate pluralization
      messages.append('both {}{}'.format(rationaleLowerCase, rationalePlural))
    if reason == 'Style':
      messages.append('both in the {} style'.format(rationaleLowerCase))
    if reason == 'Movement':
      messages.append('in the {} movement'.format(rationale))
    if reason == 'SocialTags':
      messages.append('have to do with {}'.format(rationale))
    
  # Add 'and'
  message_length = len(messages)
  if message_length > 1:
    messages[message_length - 1] = 'and ' + messages[message_length - 1]

  message = ', '.join(messages) if (message_length > 2) else ' '.join(messages)
  return 'These pieces are ' + message;
