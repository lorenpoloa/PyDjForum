from django.db import models

# Create your models here.

class GitRepository(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Maintainer(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='maintainers')
    repository = models.ForeignKey(GitRepository, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - ({self.role})"

class Deck(models.Model):
    link = models.URLField(unique=True)

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    repository = models.ForeignKey(GitRepository, on_delete=models.CASCADE, related_name='projects', null=True, blank=True) 
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)    
    maintainer = models.ForeignKey(Maintainer, on_delete=models.SET_NULL, null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

