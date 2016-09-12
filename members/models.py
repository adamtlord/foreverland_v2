from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField

SECTIONS = (
    ('v', 'Vocal'),
    ('h', 'Horn'),
    ('r', 'Rhythm')
)


class Member(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    display_first = models.CharField(max_length=50, blank=True, null=True)
    display_last = models.CharField(max_length=50, blank=True, null=True)
    instrument = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True, choices=SECTIONS)
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    join_date = models.DateField(verbose_name="Date of Joining", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    active = models.BooleanField()
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Zip", max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    ssn = models.CharField(verbose_name="SSN#", max_length=16, blank=True, null=True)
    partner = models.BooleanField(default=False)
    date_partner_joined = models.DateField(verbose_name="Became a Partner", blank=True, null=True)
    date_partner_left = models.DateField(verbose_name="Left Partnership", blank=True, null=True)

    class Meta:
        ordering = ['-active', '-section', 'display_first']
    def __unicode__(self):
        return '%s %s' % (self.display_first, self.display_last)


class Sub(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    instrument = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Zip", max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    ssn = models.CharField(verbose_name="SSN#", max_length=16, blank=True, null=True)

    class Meta:
        ordering = ['first_name']

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)
