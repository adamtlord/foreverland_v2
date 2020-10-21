from django import forms

from media.models import Image


class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        self.fields['albums'].widget.attrs['class'] = 'form-control'
