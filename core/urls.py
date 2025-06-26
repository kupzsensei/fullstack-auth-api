"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView

from .views import RegisterView , GetAllUserView

from django.conf import settings
from django.conf.urls.static import static

from overtime.views import FileUploadView, RequestOvertimeView , RequestApprovalView ,EvidenceApprovalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/auth/register/' ,RegisterView.as_view() ),
    path('api/auth/users/' ,GetAllUserView.as_view()),

    # Overtime
    path('api/overtime/' , RequestOvertimeView.as_view()),
    path('api/request-approval/' , RequestApprovalView.as_view()),
    path('api/evidence-approval/' , EvidenceApprovalView.as_view()),

    path('api/fileupload/' , FileUploadView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
