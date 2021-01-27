from .models import Log


class LoggingMiddleware:
    actions = {
        'GET': 'List',
        'POST': 'Create',
        'PATCH': 'Update',
        'DELETE': 'Destroy'
    }
    models = {
        'register': 'User',
        'students': 'Student',
        'schools': 'School'
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.username:
            username = 'AnonymousUser'
        else:
            username = request.user.username

        url = request.get_raw_uri().split('/')[-2]
        logs = request.get_raw_uri().split('/')[-3]
        urls = ['register', 'students', 'schools']

        if url in urls and logs != 'logs':
            Log.objects.create(
                model=self.models[url],
                username=username,
                status_code=response.status_code,
                action=self.actions[request.method],
                data=response.data
                )

        return response
