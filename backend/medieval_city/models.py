from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Prefetch, Count


class CityQuerySet(models.QuerySet):
    def prefetch_civilians(self):
        civilians = Prefetch(
            'civilians',
            queryset=Civilian.objects.all()
        )

        return self.prefetch_related(civilians)


class City(models.Model):
    name = models.CharField(
        'Название города',
        max_length=100,
    )

    objects = CityQuerySet.as_manager()

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'Город "{self.name}"'


class Estate(models.Model):
    class_name = models.CharField(
        'Название сословия',
        max_length=200
    )

    class Meta:
        verbose_name = 'Сословие'
        verbose_name_plural = 'Сословия'

    def __str__(self):
        return self.class_name


class Vassal(models.Model):
    subordinate = models.ForeignKey(
        'Civilian',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='seniors'
    )

    def __str__(self):
        return f'{self.subordinate.name} {self.subordinate.surname}'


class Civilian(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200,
    )
    surname = models.CharField(
        'Фамилия',
        max_length=200,
    )
    age = models.PositiveIntegerField(
        'Возраст'
    )
    portrait = models.ImageField(
        'Портрет',
        blank=True,
        null=True
    )
    estate = models.ForeignKey(
        Estate,
        on_delete=models.PROTECT,
        verbose_name='Сословие',
        related_name='civilians'
    )
    senior = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Сеньор',
        related_name='vassals',
    )
    vassal = models.ManyToManyField(
        Vassal,
        blank=True,
        null=True,
        related_name='vassals',
        verbose_name='Вассал'
    )
    income = models.DecimalField(
        'Доход',
        blank=True,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    city = models.ForeignKey(
        City,
        verbose_name='Город проживания',
        related_name='civilians',
        on_delete=models.CASCADE
    )


    class Meta:
        verbose_name = 'Горожанин'
        verbose_name_plural = 'Горожане'

    def __str__(self):
        return f'{self.name} {self.surname}'
