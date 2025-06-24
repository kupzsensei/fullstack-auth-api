from rest_framework import serializers
from .models import Overtime , FileUpload , OvertimeFile , Comment

class OvertimePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = ['reason' ,'time_in' , 'time_out' , 'supervisor']