"""
A helper command to do an actual pipeline run.
"""

from django.core.management.base import BaseCommand

from dswapi.services.etl_pipeline import execute_pipeline


class Command(BaseCommand):
    help = 'Executes the full ETL pipeline.'

    def handle(self, *args, **options):
        execute_pipeline()
