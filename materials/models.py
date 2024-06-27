from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='название курса')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=50, verbose_name='описание курса', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='название урока')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=50, verbose_name='описание курса', **NULLABLE)
    url = models.CharField(max_length=50, verbose_name='ссылка', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.url}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class SubForCourseUpdate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.user} {self.course}'

    class Meta:
        verbose_name = 'подписка на курс'
        verbose_name_plural = 'подписки на курсы'
