from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from core.helpers.fields_maxlength import fields_maxlength
from ..models import Account
from ..forms.create_account import CreateAccountForm


def create(request):
    """
    Where the user can create a new account.
    """

    response = None

    if request.method == 'POST':

        create_account_form = CreateAccountForm(request.POST)

        if create_account_form.is_valid():
            account = create_account_form.create()
            request.session['create_account_email'] = account.email
            response = redirect('accounts:create:validate_email')
        else:
            context = {
                'data': create_account_form.data,
                'errors': create_account_form.errors,
                #'maxlength': fields_maxlength(
                #    Account, ['username', 'password', 'email']
                #)
            }

    else:
        context = {}

    if not response:
        response = render(
            request,
            'accounts/create/create.html',
            context
        )

    return response


def validate_email(request):
    """
    The page after a successful account creation, where the user gets
    instructions about the validation email.
    """

    email = request.session.get('create_account_email')

    return render(
        request,
        'accounts/create/validate_email.html',
        {'email': email}
    )


def completed(request):
    """
    The page the user comes to from the "validate email address" email,
    where his/her account gets validated.
    """

    success = False

    try:
        account = Account.objects.get(email=request.GET.get('email'))
    except ObjectDoesNotExist:
        pass
    else:
        if account.validate_with_token(request.GET.get('validation_token')):
            success = True

    return render(
        request,
        'accounts/create/completed.html',
        {'success': success}
    )