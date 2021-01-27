from .models import Log
from urllib.parse import urlparse


class LoggingMiddleware:
    actions = {
        'GET': 'List',
        'POST': 'Create',
        'PATCH': 'Update',
        'DELETE': 'Destroy'
    }
    models = {
        '/api/register/': 'User',
        '/api/students/': 'Student',
        '/api/schools/': 'School'
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.username:
            username = 'AnonymousUser'
        else:
            username = request.user.username

        path = urlparse(request.get_raw_uri()).path

        if path in self.models:
            Log.objects.create(
                model=self.models[path],
                username=username,
                status_code=response.status_code,
                action=self.actions[request.method],
                data=response.data
                )

        return response
