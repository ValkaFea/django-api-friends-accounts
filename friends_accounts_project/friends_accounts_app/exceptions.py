from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        return Response({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

    return response