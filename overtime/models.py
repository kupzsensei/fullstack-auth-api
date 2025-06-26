from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FileUpload(models.Model):
    file = models.FileField(upload_to='files' )
    time_stamp = models.DateTimeField(auto_now_add=True)

   

class Overtime(models.Model):
    user = models.ForeignKey(User , on_delete=models.PROTECT)
    reason = models.TextField()
    # status = models.ForeignKey('OvertimeStatus' , models.PROTECT)
    supervisor = models.ForeignKey(User , on_delete=models.CASCADE , related_name='supervisor')
    time_in = models.DateTimeField(blank=True , null=True)
    time_out = models.DateTimeField(blank=True , null=True)
    request_approval = models.BooleanField(default=False)
    evidence_approval = models.BooleanField(default=False)
    # files
    # comments

    def __str__(self):
        return self.reason

# class OvertimeStatus(models.Model):
#     name = models.CharField(unique=True)

#     def __str__(self):
#         return self.name


class OvertimeFile(models.Model):
    overtime = models.ForeignKey(Overtime , on_delete=models.CASCADE , related_name='files')
    file = models.ForeignKey(FileUpload , on_delete=models.CASCADE , null=True , blank=True)

    

class Comment(models.Model):
    comment = models.TextField()
    file = models.ForeignKey(FileUpload , on_delete=models.CASCADE , null=True , blank=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    overtime = models.ForeignKey(Overtime , on_delete=models.CASCADE , related_name='comments')

    def __str__(self):
        return self.comment