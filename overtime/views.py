from django.shortcuts import render
from rest_framework import generics
from .serializers import OvertimePostSerializer, CommentSerializer, OvertimeGetSerializer , FileUploadSerializer
from .models import Overtime , FileUpload , Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser , MultiPartParser

# Create your views here.
class RequestOvertimeView(generics.ListCreateAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimePostSerializer
    parser_classes = [FormParser , MultiPartParser]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OvertimeGetSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Overtime.objects.filter(supervisor=self.request.user)

class RequestApprovalView(APIView):
    def post(self,request):
        print('this is it' , request.data)
        instance = Overtime.objects.get(id=request.data['id'])

        if not instance:
            return Response({'error': 'request not found'} , status=404)
        
        if instance.supervisor != request.user:           
            return Response({'error': 'request fail'} , status=401)
        
        instance.request_approval = True
        instance.save()
        return Response({'ok': True})

class EvidenceApprovalView(APIView):
    def post(self,request):
        
        instance = Overtime.objects.get(id=request.data['id'])

        if not instance:
            return Response({'error': 'request not found'} , status=404)
        
        if instance.supervisor != request.user:           
            return Response({'error': 'request fail'} , status=401)
        
        instance.evidence_approval = True

        instance.save()
        return Response({'ok': True})
    

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()


class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
    