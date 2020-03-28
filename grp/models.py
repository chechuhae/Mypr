from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=u"Пользователь"
                                )
    user_name = models.CharField(max_length=15, blank=False,
                                 verbose_name=u"Имя", null=True
                                 )
    user_surname = models.CharField(max_length=15, blank=True,
                                    verbose_name=u"Фамилия", null=True
                                    )
    avatar = models.FileField(verbose_name=u"Аватар", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True,
                           verbose_name=u"О себе"
                           )
    city = models.CharField(max_length=30, blank=True, null=True,
                            verbose_name=u"Город"
                            )
    birth_date = models.DateField(null=True, blank=True,
                                  verbose_name=u"Дата рождения"
                                  )

    def my_last_cicle_first(self):
        if Cicle.objects.filter(user=self.user):
            list = []
            for cicle in Cicle.objects.filter(user=self.user):
                list.append(cicle.last_cicle_first_date)
            list = max(list)
            return list
        else:
            return "Вы не заполнили свои циклы"

    def my_last_cicle_last(self):
        if Cicle.objects.filter(user=self.user):
            list = []
            for cicle in Cicle.objects.filter(user=self.user):
                list.append(cicle.last_cicle_last_date)
            list = max(list)
            return list
        else:
            return "Вы не заполнили свои циклы"

    def how_long(self):
        if Cicle.objects.filter(user=self.user):
            for cicle in Cicle.objects.filter(user=self.user):
                if cicle.last_cicle_first_date == self.my_last_cicle_first():
                    return cicle.timer()


class Cicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=u"Пользователь", related_name='cicle'
                             )
    last_cicle_first_date = models.DateField(null=True, blank=True,
                                             verbose_name=u"Начало последнего"
                                                          u" цикла"
                                             )
    last_cicle_last_date = models.DateField(null=True, blank=True,
                                            verbose_name=u"Окончание "
                                                         u"последнего цикла"
                                            )

    def timer(self):
        timer = (self.last_cicle_first_date + timedelta(
            days=self.counter()) - date.today()).days
        if timer <= 0:
            return ("Цикл завершен")
        else:
            return timer

    def list_of_starts(self):
        list = []
        if Cicle.objects.filter(user=self.user).exists():
            for cicle in Cicle.objects.filter(user=self.user):
                list.append(cicle.last_cicle_first_date)
            list = min(list)
            return list
        else:
            return "No"

    def counter(self):
        if Cicle.objects.filter(user=self.user).exists():
            number = 0
            for cicle in Cicle.objects.filter(user=self.user):
                if cicle.list_of_ends() <= self.last_cicle_last_date:
                    number += 1
            days = (self.list_of_ends() - self.list_of_starts()).days
            if days:
                return days // (number - 1)
            else:
                days = 28
                return days
        else:
            return "No"

    def list_of_ends(self):
        if self.list_of_starts():
            if Cicle.objects.filter(user=self.user):
                if self.last_cicle_first_date >= self.list_of_starts():
                    maximum = self.last_cicle_first_date
                    return maximum
                else:
                    maximum = self.list_of_starts()
                    return maximum
            else:
                maximum = self.last_cicle_first_date
                return maximum
        else:
            return "No"

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_cicle_first_date']
