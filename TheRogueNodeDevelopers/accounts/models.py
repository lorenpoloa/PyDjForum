from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('biography'), max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        default='avatars/default.png'
    )
    
    # Campos adicionales para tu proyecto
    role = models.CharField(max_length=100, blank=True)
    github_profile = models.URLField(blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customuser_set',
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups'
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customuser_set',  # Change this to avoid conflict
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions'
    # )