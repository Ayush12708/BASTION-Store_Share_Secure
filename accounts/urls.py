from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),

    path("login/", views.login_view, name="login"),

    path("signup/", views.signup_view, name="signup"),

    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("files/", views.file_list, name="file_list"),

    path("file/<int:file_id>/", views.file_detail, name="file_detail"),

    path("upload/", views.upload_file, name="upload_file"),

    path("delete/<int:file_id>/", views.delete_file, name="delete_file"),

    path("profile/", views.profile, name="profile"),

    path("audit-logs/", views.audit_logs, name="audit_logs"),

    path("api/files/", views.api_files, name="api_files"),

    
]