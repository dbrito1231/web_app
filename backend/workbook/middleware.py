from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden


class LocalhostCorsMiddleware:
    """Allow CORS only from local Vite dev servers."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin", "")
        if request.method == "OPTIONS" and origin in settings.CORS_ALLOWED_ORIGINS:
            response = HttpResponse(status=204)
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Vary"] = "Origin"
            return response

        response = self.get_response(request)

        if origin in settings.CORS_ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Vary"] = "Origin"

        return response


class LocalOriginGuardMiddleware:
    """Reject non-local browser origins on API routes."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            origin = request.headers.get("Origin")
            if origin and origin not in settings.CORS_ALLOWED_ORIGINS:
                return HttpResponseForbidden("Origin not allowed")
        return self.get_response(request)
