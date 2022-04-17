from django import forms
from tweets.models import Status

class SettingsForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    image = forms.ImageField(required=False)

class CommentForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Status
        fields = ('status_text', 'image',)