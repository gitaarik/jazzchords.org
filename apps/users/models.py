from random import randint
from django.conf import settings
from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from core.helpers.lazy import LazyStr


class User(models.Model):

    def generate_token():
        return randint(1000000000, 9999999999)

    username = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            'blank': "Please choose a username.",
            'max_length': "A username can at most have 50 characters.",
            'unique': "Sorry, this username is already taken."
        },
        validators=[
            validators.MinLengthValidator(2,
                "A username should have at least 2 characters."
            )
        ]
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            'blank': (
                "Please fill in your email address. We use it to "
                "confirm ownership in case you lost your password."
            ),
            'max_length': "An email address can at most have 254 characters.",
            'invalid': "Sorry but this email address is not valid.",
            'unique': LazyStr(lambda: (
                "There's already an account that uses this email "
                "address. If you forgot your password, you can <a "
                "href=\"{}\">reset it over here</a>.".format(
                    reverse('users:reset_password')
                )
            ))
        }
    )

    password = models.CharField(
        max_length=50,
        error_messages={
            'blank': "Please create a password.",
            'max_length': "Please choose a password with max 50 characters.",
        },
        validators=[
            validators.MinLengthValidator(8,
                "Please choose a password that's at least 8 characters long."
            )
        ]
    )

    validated = models.BooleanField(default=False)
    validation_token = models.CharField(
        max_length=50,
        default=generate_token
    )

    def __str__(self):
        return self.username

    def send_confirmation_email(self):

        subject = "{} account creation".format(settings.WEBSITE_NAME)
        from_email = 'accounts@{}'.format(settings.DOMAIN_NAME)
        recipients = [self.email]

        message = (
            "Welcome to {}! Please click the following link to "
            "activate your account:"
            "\n\n{}".format(
                settings.WEBSITE_NAME,
                '{}{}?email={}&validation_token={}'.format(
                    settings.WEBSITE_URL,
                    reverse('users:validate_email'),
                    self.email,
                    self.validation_token
                )
            )
        )

        send_mail(subject, message, from_email, recipients)

    def send_reset_password_email(self):

        subject = "{} password reset".format(settings.WEBSITE_NAME)
        from_email = 'accounts@{}'.format(settings.DOMAIN_NAME)
        recipients = [self.email]

        message = (
            "You have requested to reset your {} account password. Go "
            "to the following page to do so:\n\n{}"
            .format(
                settings.WEBSITE_NAME,
                '{}{}?email={}&validation_token={}'.format(
                    settings.WEBSITE_URL,
                    reverse('users:reset_password:confirm'),
                    self.email,
                    self.validation_token
                )
            )
        )

        send_mail(subject, message, from_email, recipients)
