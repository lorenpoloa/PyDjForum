from django.db import models
from accounts.models import CustomUser

    
class DocTopic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class DocSection(models.TextChoices):
    PROJECT = 'PR', 'Project'
    PLATFORM = 'PL', 'Platform'
    NETWORK = 'NE', 'Network'
    PROTOCOLS = 'PT', 'Protocols'
    APPLICATION = 'AP', 'Application'
    SERVICES = 'SE', 'Services'
    SECURITY = 'SEC', 'Security'
    DATABASES = 'DB', 'Databases'
    TOOLS = 'TO', 'Tools'
    DEVOPS = 'DO', 'DevOps'
    CLOUD = 'CL', 'Cloud'
    AI = 'AI', 'Artificial Intelligence'
    MACHINE_LEARNING = 'ML', 'Machine Learning'
    DATA_SCIENCE = 'DS', 'Data Science'
    WEB_DEVELOPMENT = 'WD', 'Web Development'
    MOBILE_DEVELOPMENT = 'MD', 'Mobile Development'

class ProcessState(models.TextChoices):
    DEVELOPMENT = 'DE', 'Development'
    PRODUCTION = 'PR', 'Production'


# Create your models here.
class Documentation(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    version = models.CharField(max_length=50)
    is_public = models.BooleanField(default=False)
    section = models.CharField(
        max_length=3,
        choices=DocSection.choices,
        default=DocSection.NETWORK
    )
    process_state = models.CharField(
        max_length=2,
        choices=ProcessState.choices,
        default=ProcessState.DEVELOPMENT
    )
    doc_topic = models.ForeignKey(
        DocTopic,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.title} (v{self.version})"