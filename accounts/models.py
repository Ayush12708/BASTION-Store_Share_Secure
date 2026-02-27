# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Users(models.Model):
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    storage_limit = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        
class AuditLogs(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    
    file = models.ForeignKey(
        'Files',
        models.SET_NULL,
        blank=True,
        null=True
    )

    action_type = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    action_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_logs'
class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class FileVersions(models.Model):
    file = models.ForeignKey('Files', models.DO_NOTHING)
    version_number = models.IntegerField()
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file_versions'
        unique_together = (('file', 'version_number'),)
        
        
class Files(models.Model):

    file_name = models.CharField(max_length=255)
    id = models.BigAutoField(primary_key=True) 

    file_url = models.CharField(max_length=500)

    file_size = models.BigIntegerField()

    upload_time = models.DateTimeField()

    owner = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'files'


class Permissions(models.Model):
    file = models.ForeignKey(Files, models.DO_NOTHING)
    id = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey('Users', models.DO_NOTHING)
    permission_type = models.CharField(max_length=5)
    expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'
        unique_together = (('file', 'user'),)
