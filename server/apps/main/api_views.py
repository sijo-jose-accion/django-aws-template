import json
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .permissions import ContactMessagePermission
from .tasks import send_contact_me_notification

class APIMessageViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = (ContactMessagePermission,)


    def get_queryset(self):
        """
        This view should return a list of all records
        for the currently authenticated user.
        """
        #user = self.request.user
        return ContactMessage.objects.all()

    def perform_create(self, serializer):
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save()

        # Schedule a task to send email
        send_contact_me_notification(instance)

