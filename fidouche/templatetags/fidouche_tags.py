from django import template
from django.forms import PasswordInput

register = template.Library()

@register.filter(name='is_password')
def is_password(field):
  return field.field.widget.__class__.__name__ == PasswordInput().__class__.__name__
