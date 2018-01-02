from django import forms
from .validators import validate_file_extension

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255)
    file = forms.FileField(validators=[validate_file_extension])