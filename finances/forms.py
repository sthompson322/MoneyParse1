from django import forms
from .models import Income, Transaction

CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Rent', 'Rent'),
    ('Utilities', 'Utilities'),
    ('Transportation', 'Transportation'),
    ('Entertainment', 'Entertainment'),
    ('Miscellaneous', 'Miscellaneous'),
]

class TransactionForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'with_who_or_what', 'date']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget = forms.Select(
            choices=[(True, '+'), (False, '−')],
            attrs={'class': 'form-select'}
        )
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['with_who_or_what'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
