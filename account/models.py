from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager


class TimeStampAbstractModel(models.Model):
    
    created_at = models.DateTimeField(_('дата добавления'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата изменения'), auto_now=True)

    class Meta:
        abstract = True


class Group(TimeStampAbstractModel):
    
    class Meta:
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
        ordering = ('-created_at', '-updated_at')  
    
    title = models.CharField(_('название'), max_length=250, unique=True)
    
    def __str__(self):
        return f'{self.title}'

  
class User(TimeStampAbstractModel, AbstractUser):
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ('-date_joined',)      
    
    STAFF = 'is_staff'
    HEAD = 'is_head'
    HEAD_TITLE = _('Советник')
    STAFF_TITLE = _('Сотрудник')
    
    ROLES = (
        (STAFF, STAFF_TITLE),
        (HEAD, HEAD_TITLE),
    )
        
    username = None
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'],
        upload_to='avatars/', force_format='WEBP', quality=90, 
        verbose_name=_('аватарка'), null=True, blank=True) 
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name=_('номер телефона'))
    email = models.EmailField(blank=True, verbose_name=_('электронная почта'), unique=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name=_('группа'),
        related_name='users', blank=True, null=True)
    point = models.PositiveIntegerField(_('баллы'), default=0)
    role = models.CharField(_('роль'), default=STAFF, max_length=50, choices=ROLES, blank=True)
    last_activity = models.DateTimeField(blank=True, 
        null=True, verbose_name=_('последнее действие'))
  
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'
    get_full_name.fget.short_description = _('полное имя') 
    
    def __str__(self):
        return f'{self.get_full_name or str(self.phone)}'
    
    
class RegistrationCode(TimeStampAbstractModel):
    
    class Meta:
        verbose_name = _('регистрационный код')
        verbose_name_plural = _('регистрационный код')
        ordering = ('-created_at', '-updated_at')
        
    code = models.PositiveSmallIntegerField(_('код'), unique=True,
                validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    note = models.CharField(_('заметка'), max_length=255, blank=True, null=True)
    role = models.CharField(_('роль'), default=User.STAFF, 
                max_length=50, choices=User.ROLES, blank=True)
    
    def __str__(self):
        return f'{self.role} - {self.code}'
    
        
    
# Create your models here.