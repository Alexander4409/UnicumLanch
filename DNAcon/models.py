from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    group = models.CharField(max_length=10)
    Project_type = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='image/')
    video = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    task_file = models.FileField(
        upload_to='task/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])]
    )
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_file = models.FileField(
        upload_to='homeWork/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])]
    )
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_file.name
