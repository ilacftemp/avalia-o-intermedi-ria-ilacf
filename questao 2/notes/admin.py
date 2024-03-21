from django.contrib import admin
from .models import Note, Tag, Fact


admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(Fact)