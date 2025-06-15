from django.db import models
from apps.accounts.models import CustomUser

# Create your models here.
class Documentation(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    version = models.CharField(max_length=50)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (v{self.version})"