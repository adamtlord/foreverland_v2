from django.db import models
from shows.models import Show


class Testimonial(models.Model):
	"""Quotes from past shows"""
	quote = models.TextField()
	source = models.CharField(max_length=100, blank=True, null=True)
	show = models.ForeignKey(Show, blank=True, null=True, related_name="testimonial")
	featured = models.BooleanField(default=False)

	def __unicode__(self):
		return self.quote
