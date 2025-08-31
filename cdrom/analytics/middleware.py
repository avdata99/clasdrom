import logging
import time
from analytics.models import RequestLog


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip logging for static files and admin media
        if self.should_skip_logging(request):
            return self.get_response(request)

        start_time = time.time()

        # Capture POST data before processing request to avoid stream consumption
        post_params = ""
        if request.method == "POST":
            try:
                post_params = request.body.decode('utf-8')
            except Exception:
                post_params = ""

        # Process the request
        response = self.get_response(request)

        # Calculate response time
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Log the request
        self.log_request(request, response, response_time, post_params)

        return response

    def should_skip_logging(self, request):
        """Skip logging for certain paths to avoid noise"""
        skip_paths = [
            '/static/',
            '/media/',
            '/favicon.ico',
            '/admin/jsi18n/',
        ]
        return any(request.path.startswith(path) for path in skip_paths)

    def log_request(self, request, response, response_time, post_params):
        """Log the request data to the database"""
        try:
            # Get IP address
            ip_address = self.get_client_ip(request)

            # Get user if authenticated
            user = request.user if request.user.is_authenticated else None

            RequestLog.objects.create(
                user=user,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                method=request.method,
                url=request.build_absolute_uri(),
                path=request.path,
                query_string=request.META.get('QUERY_STRING', ''),
                referer=request.META.get('HTTP_REFERER', ''),
                response_status=response.status_code,
                response_time_ms=response_time,
                post_params=post_params,
            )
        except Exception as e:
            # Silently fail to avoid breaking the application
            logger.error(f"Error logging request: {e}")

    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
