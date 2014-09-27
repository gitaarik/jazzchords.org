from django.shortcuts import render, redirect
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.urlresolvers import reverse

from core.helpers.fields_maxlength import fields_maxlength
from ..models import Account


def request(request):
    """
    The user requests a password reset.
    """

    email = request.POST.get('email') or ''
    errors = []
    response = None

    if request.method == 'POST':

        if not email:
            errors = ["Please fill in your email address."]
        else:

            validate_email = django_validate_email
            validate_email.message = "Please enter a valid email address."

            try:
                validate_email(email)
            except ValidationError as error:
                errors = error.messages

        if not errors:

            try:
                account = Account.objects.get(email=email)
            except ObjectDoesNotExist:
                errors = [
                    "There is no account with this email address. You "
                    "can <a href=\"{}\">create<a> it if you like."
                    .format(reverse('accounts:create:create'))
                ]
            else:
                account.reset_password_request()
                response = redirect('accounts:reset_password:requested')
                request.session['reset_password_email'] = email

    if not response:

        response = render(
            request,
            'accounts/reset_password/request.html',
            {
                'email': email,
                'errors': errors,
                'maxlength': fields_maxlength(Account, ['email'])
            }
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
        response = confirm_valid(request)
    else:
        response = render(
            request,
            'accounts/reset_password/invalid_token.html'
        )

    return response

def confirm_valid(request):
    """
    The page a validated user comes to from the password reset email.
    """

    response = None
    errors = {}

    if request.method == 'POST':

        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        account._meta.get_field('password').error_messages['blank'] = (
            "Please fill in your new password."
        )

        if not new_password2:
            errors['new_password2'] = ["Please repeat your new password."]

        if not errors and new_password1 != new_password2:
            errors['new_password1'] = [
                "Sorry, the passwords don't match. Please try it "
                "again."
            ]

        account.password = new_password1

        try:
            account.full_clean()
        except ValidationError as error:

            if 'new_password1' not in errors:
                errors['new_password1'] = []

            errors['new_password1'].extend(
                error.message_dict['password']
            )

        if not errors:
            account.save()
            response = redirect('accounts:reset_password:completed')

    if not response:

        response = render(
            request,
            'accounts/reset_password/confirm.html',
            {
                'errors': errors,
                'maxlength': fields_maxlength(Account, ['password'])
            }
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