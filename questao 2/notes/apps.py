from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'

class TagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'

class FactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facts'