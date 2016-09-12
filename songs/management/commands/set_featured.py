from django.core.management.base import BaseCommand
from songs.models import Song

class Command(BaseCommand):
	def handle(self, *args, **options):
		songs = Song.objects.all()
		for song in songs:
			song.display = True
			song.save()