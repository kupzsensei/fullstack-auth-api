from django.shortcuts import render
from rest_framework import generics
from .serializers import OvertimePostSerializer
from .models import Overtime

# Create your views here.
class RequestOvertimeView(generics.ListCreateAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimePostSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return Overtime.objects.filter(supervisor=self.request.user)