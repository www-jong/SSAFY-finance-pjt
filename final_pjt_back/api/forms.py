from django import forms
from .models import ExchangeInfo

class ExchangeInfoForm(forms.ModelForm):
    class Meta:
        model = ExchangeInfo
        fields = '__all__'  # 모든 필드를 폼에 포함
        exclude = ('exchangeDate',)