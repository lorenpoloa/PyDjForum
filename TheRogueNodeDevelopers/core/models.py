from django.db import models

# Create your models here.
class Information(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {'Public' if self.is_public else 'Private'}"