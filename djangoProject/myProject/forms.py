from myProject.models import Order
from datetime import date
from django.core.exceptions import ValidationError
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ("number","monitor","amount","order_date","provider","region")
        widgets = {
            "order_date": DatePickerInput(options={"format": "MM/DD/YYYY"}),
        }

    def clean_order_date(self):
        date_local = self.cleaned_data["order_date"]
        amount = self.cleaned_data["amount"]
        if amount > 7 and date_local > date.today().day:
            raise ValidationError("Вы уверены, что хотите заказать? Посылка может задержаться.")
        return date_local

    def clean(self):
        duplicates = Order.objects.filter(number=self.cleaned_data["number"])
        if duplicates.exists():
            raise ValidationError('Номер должен быть уникальным!')


"""
class OrderForm(forms.Form):
    monitor = forms.CharField(help_text="Введите название монитора")
    number = forms.IntegerField(help_text="Введите номер заказа",min_value=1,max_value=5)
    amount = forms.IntegerField(help_text="Введите количество",min_value=1,max_value=10)
    order_date = forms.DateField(help_text="Введите дату оформления заказа")
    provider = forms.CharField(help_text="Введите поставщика") 
"""