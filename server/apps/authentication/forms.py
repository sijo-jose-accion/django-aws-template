import pytz

from captcha.fields import ReCaptchaField

from django import forms as forms
from django.forms import ModelForm
from django.conf import settings
from django.core.exceptions import ValidationError

from allauth.account.forms import SignupForm

from .models import Account


class TimeZoneFormField(forms.TypedChoiceField):
    def __init__(self, *args, **kwargs):

        def coerce_to_pytz(val):
            try:
                return pytz.timezone(val)
            except pytz.UnknownTimeZoneError:
                raise ValidationError("Unknown time zone: '%s'" % val)

        defaults = {
            'coerce': coerce_to_pytz,
            'choices': [(tz, tz) for tz in pytz.common_timezones],
            'empty_value': None,
        }
        defaults.update(kwargs)
        super(TimeZoneFormField, self).__init__(*args, **defaults)


class AccountUpdateForm(ModelForm):
    time_zone = TimeZoneFormField()
    class Meta:
        model = Account
        fields = ['username', 'name', 'tagline']

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['username'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        self.fields['name'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        self.fields['tagline'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        tz = settings.TIME_ZONE
        if 'instance' in kwargs:
            user = kwargs['instance']
            if user and user.time_zone:
                tz = user.time_zone
        self.initial['time_zone'] = tz
        self.fields['time_zone'].widget.attrs['class'] = 'custom-form-element custom-select'


class AllauthSignupForm(SignupForm):
    """Base form for django-allauth to use, adding a ReCaptcha function"""
    captcha = ReCaptchaField()
