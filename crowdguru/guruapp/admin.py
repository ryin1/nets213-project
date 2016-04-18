from django.contrib import admin

# Register your models here.

from .models import Category, Achievement, Item, Question, Recommendation

admin.site.register(Category)
admin.site.register(Achievement)
admin.site.register(Item)
admin.site.register(Question)
admin.site.register(Recommendation)