from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms

from portfolio.models import Feedback


class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class':'form-control ml-2 mr-2'}))

    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
        }