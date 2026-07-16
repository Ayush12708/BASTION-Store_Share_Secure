from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50)
    storage_limit = models.BigIntegerField(default=0)

    class Meta:
        db_table = "users"


class Files(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="files"
    )

    class Meta:
        db_table = "files"


class FileVersions(models.Model):
    file = models.ForeignKey(
        Files,
        on_delete=models.CASCADE
    )

    version_number = models.IntegerField()
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "file_versions"
        unique_together = ("file", "version_number")


class Permissions(models.Model):
    file = models.ForeignKey(
        Files,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )

    permission_type = models.CharField(max_length=5)
    expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "permissions"
        unique_together = ("file", "user")


class AuditLogs(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    file = models.ForeignKey(
        Files,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action_type = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    action_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
