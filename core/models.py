from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import User


class TimeStampAbstractModel(models.Model):
    
    created_at = models.DateTimeField(_('дата добавления'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата изменения'), auto_now=True)

    class Meta:
        abstract = True
        

class Point(TimeStampAbstractModel):
    
    MONTHS = (
        (1, 'Январь'),
        (2, 'Февраль'),
        (3, 'Март'),
        (4, 'Апрель'),
        (5, 'Май'),
        (6, 'Июнь'),
        (7, 'Июль'),
        (8, 'Август'),
        (9, 'Сентябрь'),
        (10, 'Октябрь',),
        (11, 'Ноябрь',),
        (12, 'Декабрь',),
    )
    
    class Meta:
        verbose_name = _('балл')
        verbose_name_plural = _('баллы')
        ordering = ('-created_at', '-updated_at')
        
    head = models.ForeignKey(User, on_delete=models.PROTECT, 
                verbose_name=_('директор'), related_name='put_points')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, 
                verbose_name=_('сотрудник'), related_name='points_as_staff')
    value = models.PositiveIntegerField(_('балл'))
    month = models.PositiveIntegerField(_('месяц'), choices=MONTHS)
    year = models.PositiveIntegerField(_('год'), 
                validators=[MinValueValidator(1999), MaxValueValidator(2099)])
    
    def clean(self):
        if self.head.role != User.HEAD:
            raise ValidationError(f'{self.head} должен быть {User.HEAD_TITLE}')
        
        if self.staff.role != User.STAFF:
            raise ValidationError(f'{self.staff} должен быть {User.STAFF_TITLE}')
        
        point = Point.objects.filter(month=self.month, year=self.year, head=self.head, staff=self.staff)
        if point.exists() and point.first().id != self.id:
            raise ValidationError(f'Балл в {self.month}-{self.year} с {self.head} уже существует')
        
        if self.id is None:
            if self.head.point - self.value < 0:
                raise ValidationError(f'У советника "{self.head}" не достаточно баллов для выдиления')
            self.head.point -= self.value
            self.head.save()
        else:
            point = Point.objects.get(id=self.id)
            if self.value > point.value:
                avarage_point = self.value - point.value
                if avarage_point > self.head.point:
                    raise ValidationError(f'У советника "{self.head}" не достаточно баллов для выдиления')
                self.head.point -= avarage_point
                self.head.save()
            else:
                avarage_point = point.value - self.value
                self.head.point += avarage_point
                self.head.save()
                 
    def __str__(self) -> str:
        return f'{self.head} - {self.staff}'

# Create your models here.
