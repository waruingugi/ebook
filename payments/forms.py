from django import forms
from payments.models import Customers


class TransactionCodeForm(forms.Form):

    transaction_code = forms.CharField(
            widget=forms.TextInput(
                attrs={'name': 'transaction_code'}
            )
    )

    def clean(self, *args, **kwargs):
        """Check if transaction code has been used before."""
        transaction_code = self.cleaned_data.get('transaction_code')

        transaction_code_qs = Customers.objects.filter(transaction_code=transaction_code)

        if transaction_code_qs.exists():
            self.add_error(
                'transaction_code',
                'Sorry, this transaction code has already been used!'
            )


class DetailsForm(forms.ModelForm):

    class Meta:
        model = Customers
        fields = ['name', 'email']

    def clean(self, *args, **kwargs):
        """Check if email has been used before."""
        email = self.cleaned_data.get('email')

        email_qs = Customers.objects.filter(email=email)

        if email_qs.exists():
            self.add_error(
                'email',
                'Sorry, that email has already been used!'
            )
