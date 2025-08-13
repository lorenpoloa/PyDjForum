from django.db import models

class InfoSection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

# Create your models here.
class Information(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    info_section = models.ForeignKey(
        InfoSection,
        on_delete=models.CASCADE,
        related_name='information',
        null=True,
        blank=True
    )   
    
    def __str__(self):
        return f"{self.title} - {'Public' if self.is_public else 'Private'}"