from rest_framework import serializers
from .models import Overtime , FileUpload , OvertimeFile , Comment
from core.serializers import GetUserSerializer

class OvertimePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = ['reason' ,'time_in' , 'time_out' , 'supervisor']

class OvertimeGetSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    supervisor = GetUserSerializer(read_only=True)

    class Meta:
        model = Overtime
        fields = ['reason' ,'time_in' , 'time_out' , 'supervisor','user' , 'files']
        depth = 2

