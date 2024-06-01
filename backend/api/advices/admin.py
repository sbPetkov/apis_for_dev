from django.contrib import admin
from .models import Advice


class AdviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'position')
    ordering = ('position',)


admin.site.register(Advice, AdviceAdmin)
