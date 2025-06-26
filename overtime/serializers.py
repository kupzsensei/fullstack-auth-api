from rest_framework import serializers
from .models import Overtime , FileUpload , OvertimeFile , Comment
from core.serializers import GetUserSerializer

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'

class OvertimePostSerializer(serializers.ModelSerializer):
    # files = FileUploadSerializer(required=False , many=True)
    class Meta:
        model = Overtime
        fields = ['reason' ,'time_in' , 'time_out' , 'supervisor']

    def create(self, validated_data):
        files = self.context['request'].FILES.getlist('files')
        print(files, 'this is my file')

        overtime = Overtime.objects.create(**validated_data)

        for file_instance in files: # `file_instance` is already the UploadedFile object
            try:
                # `file_instance` is directly usable by FileField
                my_file = FileUpload.objects.create(file=file_instance)
                OvertimeFile.objects.create(file=my_file, overtime=overtime)
                # Removed my_file.save() as it's redundant after create()
            except Exception as e:
                print(f"Error saving file {file_instance.name}: {e}")
                # Consider more robust error handling here if a file fails to save
                # (e.g., rollback the overtime creation or log the specific file error)
        return overtime
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class OvertimeGetSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    supervisor = GetUserSerializer(read_only=True)

    class Meta:
        model = Overtime
        fields = ['id' , 'reason' ,'time_in' , 'time_out' , 'supervisor','user' , 'files', 'request_approval','evidence_approval']
        depth = 2

