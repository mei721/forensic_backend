from django.shortcuts import render
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

class LogView(APIView):

    def get(self, request, format=None):
        # Paths to the log files
        error_log_file = os.path.join(settings.BASE_DIR, 'logs', 'error.log')
        info_log_file = os.path.join(settings.BASE_DIR, 'logs', 'info.log')

        logs = []

        # Read the error log file if it exists
        if os.path.exists(error_log_file):
            with open(error_log_file, 'r', encoding='utf-8') as f:
                logs.extend(f.readlines())  # Add the error logs to the list
        else:
            logs.append("Error log file does not exist.")

        # Read the info log file if it exists
        if os.path.exists(info_log_file):
            with open(info_log_file, 'r', encoding='utf-8') as f:
                logs.extend(f.readlines())  # Add the info logs to the list
        else:
            logs.append("Info log file does not exist.")

        # Only return the last 100 logs for performance reasons
        logs = logs[-100:]

        return Response({"logs": logs})
