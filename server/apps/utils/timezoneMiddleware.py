__author__ = 'dkarchmer'

import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')

        if not tzname:
            # Get it from the Account. Should hopefully happens once per session
            user = request.user
            if user and not user.is_anonymous():
                tzname = user.time_zone
                if tzname:
                    request.session['django_timezone'] = tzname

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()