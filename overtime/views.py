from django.shortcuts import render
from rest_framework import generics
from .serializers import OvertimePostSerializer, OvertimeGetSerializer
from .models import Overtime

# Create your views here.
class RequestOvertimeView(generics.ListCreateAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimePostSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OvertimeGetSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Overtime.objects.filter(supervisor=self.request.user)