from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptios so far")


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_request_time = {}

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        if ip_address in self.last_request_time:
            last_request_time = self.last_request_time[ip_address]
            time_since_last_request = datetime.now() - last_request_time
            if time_since_last_request < timedelta(seconds=1):
                return HttpResponse('Too many requests from this IP address', status=429)

        self.last_request_time[ip_address] = datetime.now()

        response = self.get_response(request)
        return response