from django import forms
from .validators import validate_input_file_extension


class UploadInputFileForm(forms.Form):
    """ Upload input file """
    title = forms.CharField(max_length=255)
    file = forms.FileField(validators=[validate_input_file_extension])


class UploadAlgorithmFileForm(forms.Form):
    """ Upload algorithm file """
    title = forms.CharField(max_length=255)
    file = forms.FileField(validators=[validate_input_file_extension])