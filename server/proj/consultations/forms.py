from django import forms


class UploadFileForm(forms.Form):
    img = forms.FileField()

