from django.shortcuts import render, redirect
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from ..models import Account
from ..forms import ResetPasswordRequestForm, ResetPasswordConfirmForm


def request(request):
    """
    The user requests a password reset.
    """

    response = None
    reset_password_request_form = ResetPasswordRequestForm(request.POST)

    context = {
        'fields': reset_password_request_form.fields
    }

    if request.method == 'POST':

        account = reset_password_request_form.reset_password_request()

        if account:
            response = redirect('accounts:reset_password:requested')
            request.session['reset_password_email'] = account.email
        else:
            context.update({
                'data': reset_password_request_form.data,
                'errors': reset_password_request_form.errors
            })

    if not response:

        response = render(
            request,
            'accounts/reset_password/request.html',
            context
        )

    return response

def requested(request):
    """
    The page after a successful password reset request, where the user
    get's instructed to check his email for further instructions.
    """

    email = request.session.get('reset_password_email')

    return render(
        request,
        'accounts/reset_password/requested.html',
        {'email': email}
    )

def confirm(request):
    """
    The page a user comes to from the password reset email.
    """

    email = request.GET.get('email')
    validation_token = request.GET.get('validation_token')
    valid = False

    try:
        account = Account.objects.get(email=email)
    except ObjectDoesNotExist:
        account = None
    else:
        if account.validation_token == validation_token:
            valid = True

    if valid:
        response = confirm_valid(request, account)
    else:
        response = render(
            request,
            'accounts/reset_password/invalid_token.html'
        )

    return response

def confirm_valid(request, account):
    """
    The page a validated user comes to from the password reset email.
    """

    response = None
    reset_password_confirm_form = (
        ResetPasswordConfirmForm(request.POST, account)
    )
    context = {
        'fields': reset_password_confirm_form.fields
    }

    if request.method == 'POST':

        if reset_password_confirm_form.reset_password():
            response = redirect('accounts:reset_password:completed')
        else:
            context.update({
                'data': reset_password_confirm_form.data,
                'errors': reset_password_confirm_form.errors,
                'errors_all': reset_password_confirm_form.errors.get('__all__')
            })

    if not response:

        response = render(
            request,
            'accounts/reset_password/confirm.html',
            context
        )

    return response

def completed(request):
    """
    The page the user sees when the password reset has been completed.
    """

    return render(
        request,
        'accounts/reset_password/completed.html',
    )
