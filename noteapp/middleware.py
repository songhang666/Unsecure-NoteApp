# noteapp/middleware.py
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)

        resp["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        resp["X-Frame-Options"] = "DENY"   

        resp["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' https://cdnjs.cloudflare.com 'unsafe-inline'; "
            "script-src 'self' https://cdnjs.cloudflare.com; "
            "font-src 'self' https://cdnjs.cloudflare.com data:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
        )
        return resp
