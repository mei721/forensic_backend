from django.shortcuts import render
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class LogView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # Paths to the log files
        info_log_file = os.path.join(settings.BASE_DIR, 'logs/logs', 'info.log')

        logs = []

        try:
            # Read the info log file if it exists
            if os.path.exists(info_log_file):
                with open(info_log_file, 'r', encoding='utf-8') as f:
                    logs.extend(f.readlines())  # Add the info logs to the list
            else:
                logs.append("Info log file does not exist.")
            
            # Only return the last 100 logs for performance reasons
            logs = logs[-100:]

            return Response({"logs": logs})

        except Exception as e:
            # Log the exception and return a user-friendly message
            return Response({"error": "An error occurred while retrieving the logs."}, status= 500)

