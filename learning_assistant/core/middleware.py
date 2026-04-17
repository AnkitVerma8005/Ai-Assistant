from django.http import JsonResponse
from .exceptions import LearningAssistantException
import logging

logger = logging.getLogger(__name__)

class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        import json
        if isinstance(exception, LearningAssistantException):
            return JsonResponse(
                {'error': exception.message},
                status=exception.status_code
            )
        
        if isinstance(exception, json.JSONDecodeError):
            return JsonResponse(
                {'error': "Invalid JSON format in response or request."},
                status=400
            )
        
        # Log unhandled exceptions
        logger.exception("Unhandled exception occurred: %s", str(exception))
        
        # Return JSON for all exceptions to prevent frontend parsing errors
        return JsonResponse(
            {'error': "An internal server error occurred. Please contact support."},
            status=500
        )
