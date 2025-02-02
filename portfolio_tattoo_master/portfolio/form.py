from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms

from portfolio.models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Form for user feedback submission with CAPTCHA validation.
    """

    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control ml-2 mr-2'}))

    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your message'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Telegram username'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your WhatsApp number'}),
        }