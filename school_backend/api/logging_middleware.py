from .mongodb_connector import col


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.username:
            username = 'AnonymousUser'
        else:
            username = request.user.username
        col.insert_one({username: request.method})
        return response
