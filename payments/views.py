from django.shortcuts import render
from django.http import HttpRequest
from payments.forms import (
    TransactionCodeForm, DetailsForm
)
from payments.sub_logger import logger
from payments.tasks import validate_transaction
from django.shortcuts import redirect
from payments.models import Customers


def index(request):
    assert isinstance(request, HttpRequest)
    logger.info('views.index')

    transactioncode_form = TransactionCodeForm(request.POST or None)

    if transactioncode_form.is_valid():
        logger.info('views.index: Transaction code is valid')
        transaction_code = transactioncode_form.cleaned_data.get('transaction_code')

        user_has_paid = validate_transaction(transaction_code)

        if user_has_paid:
            logger.info('views.index: User payment was successful')
            request.session['transaction_code'] = transaction_code

            return redirect(details)
        else:
            logger.info('views.index: That transaction code does not exist')
            transactioncode_form.add_error(
                'transaction_code',
                'Sorry, that transaction code is incorrect. Check your confirmation message and try again'  # noqa
            )

    return render(
        request,
        'index.html', {'title': 'Get Your Ebook', 'form': transactioncode_form}
    )


def details(request):
    assert isinstance(request, HttpRequest)
    logger.info('views.details')

    if 'transaction_code' not in request.session:
        logger.info('views.details: No transaction_code found. Redirecting to index view')  # noqa
        return redirect(index)

    details_form = DetailsForm(request.POST or None)

    if details_form.is_valid():
        logger.info('views.details: User details are valid')
        name = details_form.cleaned_data.get('name')
        email = details_form.cleaned_data.get('email')

        transaction_code = request.session['transaction_code']

        """Save email to session"""
        request.session['email'] = email

        Customers.objects.create(name=name, email=email, transaction_code=transaction_code)

        return redirect(success)

    return render(
        request,
        'details.html', {'title': 'Almost done!', 'form': details_form}
    )


def success(request):
    assert isinstance(request, HttpRequest)
    logger.info('views.success')

    if 'email' not in request.session:
        logger.info('views.success: No email found. Redirecting to details view')  # noqa
        return redirect(details)

    email = request.session['email']

    return render(
        request,
        'success.html', {'title': 'Success!', 'email': email}
    )
