from django.contrib import auth
from django.contrib.auth import logout
from django.utils.timezone import now
from django.conf import settings

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get the last activity time from the session
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                # Convert last_activity to datetime if it's stored as string
                if isinstance(last_activity, str):
                    from django.utils.dateparse import parse_datetime
                    last_activity = parse_datetime(last_activity)
                
                # Check if the session has expired
                inactive_time = (now() - last_activity).total_seconds()
                if inactive_time > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return self.get_response(request)
            
            # Update last activity time
            request.session['last_activity'] = now()

        return self.get_response(request)
