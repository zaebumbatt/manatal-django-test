from datetime import datetime

from .mongodb_connector import schools, students, users


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
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        col = None

        if url == 'register' and request.method == 'POST':
            col = users
        elif url == 'students' and logs != 'logs':
            col = students
        elif url == 'schools' and logs != 'logs':
            col = schools

        if col:
            col.insert_one(
                {
                    date_time: {
                        'model': self.models[url],
                        'username': username,
                        'action': self.actions[request.method],
                        'status_code': response.status_code,
                        'data': response.data
                    }
                }
            )
        return response
