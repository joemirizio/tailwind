import json
import os
from django.core.management.base import BaseCommand, CommandError
from curator.models import Artwork

class Command(BaseCommand):
  help = 'Loads facts into previously loaded artwork'

  def add_arguments(self, parser):
    parser.add_argument('fact_fixture', help='Artwork fact fixture file')

  def handle(self, *args, **options):
    fact_fixture = options['fact_fixture']
    with open(fact_fixture) as json_file:
      fact_data = json.load(json_file)

      for fact in fact_data:
        pk = fact['pk']
        fact_text = fact['fields']['fact']
        Artwork.objects.filter(pk=pk).update(fact=fact_text)