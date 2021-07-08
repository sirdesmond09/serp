from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name              = models.CharField(_('first name'),max_length = 250,)
    last_name               = models.CharField(_('last name'),max_length = 250)
    phone                   = models.CharField(_('phone'), max_length = 20, null = True)
    email                   = models.EmailField(_('email'), unique=True)
    gender                  = models.CharField(_('gender'), max_length = 20, null = True)
    password                = models.CharField(_('password'), max_length = 250, null=True)
    is_receptionist         = models.BooleanField(_('receptionist'), default=False)
    is_manager         = models.BooleanField(_('manager'), default=False)
    is_admin         = models.BooleanField(_('admin'), default=False)
    is_staff         = models.BooleanField(_('staff'), default=False)
    is_superuser     = models.BooleanField(_('super user'), default=False)
    is_active        = models.BooleanField(_('active'), default=True)
    date_added      = models.DateTimeField(_('date added'), auto_now_add=True)
    
    objects = UserManager()


    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def delete(self):
        self.is_active = False
        self.save()
        return 