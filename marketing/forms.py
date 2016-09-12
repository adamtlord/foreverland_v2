from django import forms

CHOICES = [
    ('1', 'select 1'),
    ('2', 'select 2'),
    ('3', 'select 3'),
    ('4', 'select 4'),
    ('5', 'select 5'),
    ('6', 'select 6')
]


class TestForm(forms.Form):
    """
    Form used to show test fields from django-common render_form_field
    """
    text = forms.CharField(label="Normal input field")
    textarea = forms.CharField(label="Textarea field", widget=forms.Textarea)
    checkbox = forms.ChoiceField(label="Checkbox field", widget=forms.widgets.CheckboxInput)
    radio = forms.ChoiceField(label="Radio field", choices=CHOICES, widget=forms.widgets.RadioSelect)
    multiple = forms.MultipleChoiceField(label="Multiple choice field", choices=CHOICES, widget=forms.widgets.CheckboxSelectMultiple)
