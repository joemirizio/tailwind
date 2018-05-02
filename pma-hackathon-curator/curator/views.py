from django.shortcuts import render
from django.db import connection

import re
from .models import Artwork

def recommendations(request, artwork_id):
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

  return render(request, 'recommendations.html', context)

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
    messages[message_length - 1] = 'and ' + messages[message_length - 1];

  message = ', '.join(messages) if (message_length > 2) else ' '.join(messages);
  return 'These pieces are ' + message;