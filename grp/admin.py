from django.contrib import admin
from grp import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_name', 'user_surname', 'city',
                    'birth_date', 'my_last_cicle_first', 'how_long')
    list_filter = ('user_name', 'user_surname', 'city', 'birth_date')
    search_fields = ('user_name', 'user_surname')


@admin.register(models.Cicle)
class CicleAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_cicle_first_date', 'last_cicle_last_date',
                    'created', 'list_of_starts', 'list_of_ends',  'counter',
                    'timer'
                    )
    list_filter = ('user',)
    search_fields = ('user',)
