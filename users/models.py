from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    password = models.CharField(verbose_name='пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты', **NULLABLE)
    amount = models.IntegerField(verbose_name='сумма оплаты')
    ways = (
        ('card', 'картой'),
        ('cache', 'наличными'),
    )
    payment_way = models.CharField(max_length=10, default='card', choices=ways, verbose_name="способ оплаты")

    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)

    def __str__(self):
        return f'{self.user} {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
