from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from .choice import StaffCategoryChoices, WorkDayChoices


class Staff(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    inn_passport = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name=_('ИНН'))
    phone = PhoneNumberField(region="KG", max_length=15, verbose_name=_('Номер телефона'))
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name=_('Фото профиля'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Адрес'))
    schedule = models.ManyToManyField('accounts.WorkDay', related_name='workday', default='monday',
                                      verbose_name=_('График работы'))
    experience = models.CharField(max_length=25, choices=StaffCategoryChoices.choices, default='trainee', null=False,
                                  blank=False,
                                  verbose_name=_('Опыт работы'))
    black_list = models.BooleanField(default=False, verbose_name=_('Черный список'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def black_list_staff(self):
        self.black_list = True
        self.is_active = False
        self.save()

    def active_staff(self):
        self.black_list = False
        self.is_active = True
        self.save()

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.first_name} --- {self.last_name} --- {self.experience} --- {self.phone} '

    def get_absolute_url(self):
        return reverse('accounts:staff-profile', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'Staff'
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')


class WorkDay(models.Model):
    day = models.CharField(max_length=25, choices=WorkDayChoices.choices, default='monday', null=False,
                           blank=False, verbose_name=_('День недели'))

    def __str__(self):
        return self.get_day_display()

    class Meta:
        verbose_name = _('День недели')
        verbose_name_plural = _('Дни недели')
