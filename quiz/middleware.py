import logging

logger = logging.getLogger(__name__)

class LogVisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("LogVisitorMiddleware initialized")

    def __call__(self, request):
        ip = get_client_ip(request)
        print(f"Real Visitor IP: {ip} - Path: {request.path}")  # Show in terminal
        logger.info(f"Real Visitor IP: {ip} - Path: {request.path}")  # Save to log file
        return self.get_response(request)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get real external IP
    else:
        ip = request.META.get('REMOTE_ADDR')  # Fallback to normal IP
    return ip
