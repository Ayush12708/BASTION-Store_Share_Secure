from django.contrib import messages
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

import boto3
from django.conf import settings
from django.utils import timezone

from .models import Users, Files, FileVersions, AuditLogs, Permissions


# =====================================================
# AUDIT LOG HELPER FUNCTION
# =====================================================

def log_action(request, action, user=None, file=None):

    ip = request.META.get("REMOTE_ADDR")

    AuditLogs.objects.create(
        user=user,
        file=file,
        action_type=action,
        ip_address=ip,
        action_time=timezone.now()
    )


# =====================================================
# SESSION LOGIN DECORATOR
# =====================================================

def session_login_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if "user_id" not in request.session:
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper


# =====================================================
# INDEX PAGE
# =====================================================

def index(request):

    log_action(request, "OPEN_INDEX")

    return render(request, "accounts/index.html")


# =====================================================
# LOGIN VIEW
# =====================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:

            user = Users.objects.get(username=username, password=password)

            request.session["user_id"] = user.id

            log_action(request, "LOGIN", user=user)

            return redirect("dashboard")

        except Users.DoesNotExist:

            log_action(request, "FAILED_LOGIN")

            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


# =====================================================
# SIGNUP VIEW
# =====================================================

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            log_action(request, "FAILED_SIGNUP_PASSWORD")

            messages.error(request, "Passwords do not match")

            return redirect("signup")


        if Users.objects.filter(username=username).exists():

            log_action(request, "FAILED_SIGNUP_USERNAME_EXISTS")

            messages.error(request, "Username already exists")

            return redirect("signup")


        user = Users.objects.create(
            username=username,
            email=email,
            password=password,
            date_joined=timezone.now()
        )

        log_action(request, "SIGNUP", user=user)

        messages.success(request, "Account created successfully")

        return redirect("login")

    return render(request, "accounts/signup.html")


# =====================================================
# LOGOUT VIEW
# =====================================================

def logout_view(request):

    user_id = request.session.get("user_id")

    if user_id:

        user = Users.objects.get(id=user_id)

        log_action(request, "LOGOUT", user=user)

    request.session.flush()

    messages.success(request, "Logged out successfully")

    return redirect("index")


# =====================================================
# DASHBOARD VIEW
# =====================================================

@session_login_required
def dashboard(request):

    user = Users.objects.get(id=request.session["user_id"])

    log_action(request, "OPEN_DASHBOARD", user=user)

    files = Files.objects.filter(owner=user)

    return render(request, "accounts/dashboard.html", {
        "user": user,
        "files": files,
        "total_files": files.count(),
        "storage_limit": user.storage_limit,
    })


# =====================================================
# MY FILES VIEW
# =====================================================

@session_login_required
def file_list(request):

    user = Users.objects.get(id=request.session["user_id"])

    log_action(request, "OPEN_MYFILES", user=user)

    files = Files.objects.filter(owner=user).order_by("-upload_time")

    return render(request, "accounts/myfiles.html", {
        "files": files
    })


# =====================================================
# FILE DETAIL VIEW
# =====================================================

@session_login_required
def file_detail(request, file_id):

    user = Users.objects.get(id=request.session["user_id"])

    file = get_object_or_404(Files, id=file_id, owner=user)

    log_action(request, "OPEN_FILE_DETAIL", user=user, file=file)

    versions = FileVersions.objects.filter(file=file)

    logs = AuditLogs.objects.filter(file=file).order_by("-action_time")

    return render(request, "accounts/file_detail.html", {
        "user": user,
        "file": file,
        "versions": versions,
        "logs": logs
    })


# =====================================================
# VIEW FILE (OPEN S3 FILE)
# =====================================================

@session_login_required
def view_file(request, file_id):

    user = Users.objects.get(id=request.session["user_id"])

    file = Files.objects.get(id=file_id)

    log_action(request, "VIEW_FILE", user=user, file=file)

    return redirect(file.file_url)


# =====================================================
# UPLOAD FILE VIEW
# =====================================================

@session_login_required
def upload_file(request):

    user = Users.objects.get(id=request.session["user_id"])

    if request.method == "POST":

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:

            log_action(request, "FAILED_UPLOAD", user=user)

            messages.error(request, "No file selected")

            return redirect("dashboard")


        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        file_key = f"uploads/{uploaded_file.name}"

        s3.upload_fileobj(
            uploaded_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": uploaded_file.content_type}
        )

        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"

        file = Files.objects.create(
            file_name=uploaded_file.name,
            file_url=file_url,
            file_size=uploaded_file.size,
            upload_time=timezone.now(),
            owner=user
        )

        log_action(request, "UPLOAD", user=user, file=file)

        messages.success(request, "File uploaded successfully")

        return redirect("dashboard")

    return render(request, "accounts/upload.html")


# =====================================================
# DELETE FILE VIEW
# =====================================================

@session_login_required
def delete_file(request, file_id):

    if request.method == "POST":

        user = Users.objects.get(id=request.session["user_id"])

        file = get_object_or_404(Files, id=file_id, owner=user)

        log_action(request, "DELETE", user=user, file=file)

        file.delete()

        messages.success(request, "File deleted successfully")

    return redirect("dashboard")


# =====================================================
# PROFILE VIEW
# =====================================================

@session_login_required
def profile(request):

    user = Users.objects.get(id=request.session["user_id"])

    log_action(request, "OPEN_PROFILE", user=user)

    return render(request, "accounts/profile.html", {
        "user": user
    })


# =====================================================
# AUDIT LOG PAGE VIEW
# =====================================================

@session_login_required
def audit_logs(request):

    user = Users.objects.get(id=request.session["user_id"])

    log_action(request, "OPEN_AUDIT_LOGS", user=user)

    logs = AuditLogs.objects.filter(user=user).order_by("-action_time")

    return render(request, "accounts/audit_logs.html", {
        "user": user,
        "logs": logs
    })


# =====================================================
# API VIEW
# =====================================================

@session_login_required
def api_files(request):

    user = Users.objects.get(id=request.session["user_id"])

    log_action(request, "API_FILES_ACCESS", user=user)

    files = Files.objects.filter(owner=user)

    data = []

    for file in files:

        data.append({
            "id": file.id,
            "file_name": file.file_name,
            "file_url": file.file_url,
            "file_size": file.file_size,
            "upload_time": file.upload_time,
        })

    return JsonResponse({
        "status": "success",
        "user": user.username,
        "total_files": len(data),
        "files": data
    })