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

class GetCommentSerializer(serializers.ModelSerializer):
    file = FileUploadSerializer()
    class Meta:
        model = Comment
        fields = ['comment' ,'file','overtime', 'user' ]
        depth = 1

class OvertimeGetSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    supervisor = GetUserSerializer(read_only=True)
    comments = GetCommentSerializer(many=True)

    class Meta:
        model = Overtime
        fields = ['id' , 'reason' ,'time_in' , 'time_out' , 'supervisor','user' , 'files', 'request_approval','evidence_approval','comments']
        depth = 2


class CommentSerializer(serializers.ModelSerializer):
    # file = FileUploadSerializer()
    class Meta:
        model = Comment
        fields = ['comment' ,'overtime' ]
    
    def create(self, validated_data):
        # Get the single file directly using .get() instead of .getlist()
        # 'files' here refers to the 'name' attribute of your frontend input: <input name="files" type="file" />
        file_data = self.context['request'].FILES.get('files') # Use .get() for a single file
        print(f"Received file in Comment serializer create: {file_data}") # Debug print

        file_instance_for_comment = None
        if file_data: # Check if a file was actually provided
            try:
                # Create a FileUpload instance for the single file
                file_instance_for_comment = FileUpload.objects.create(file=file_data)
                print(f"Successfully saved file for Comment: {file_data.name}")
            except Exception as e:
                print(f"Error saving file for Comment {file_data.name}: {e}")
                # You might want to raise a validation error here or handle it differently

        # Create the single Comment instance
        comment = Comment.objects.create(
            file=file_instance_for_comment, # Link the single uploaded file (or None)
            **validated_data
        )

        return comment # Return the created comment instance


