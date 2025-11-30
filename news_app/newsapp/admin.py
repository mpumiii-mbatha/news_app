'''Imported Modules'''
from django.contrib import admin
from .models import Publisher, Journalist, Editor, Reader, Article

# Registered models
admin.site.register(Publisher)
admin.site.register(Journalist)
admin.site.register(Editor)
admin.site.register(Reader)
admin.site.register(Article)
