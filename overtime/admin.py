from django.contrib import admin
from .models import Comment , Overtime , OvertimeFile  , FileUpload
# Register your models here.


admin.site.register(Comment)
admin.site.register(Overtime)
admin.site.register(OvertimeFile)
# admin.site.register(OvertimeStatus)
admin.site.register(FileUpload)