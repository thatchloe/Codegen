from django.contrib import admin
from .models import Code, Resettoken

# Register Codes
admin.site.register(Code)
admin.site.register(Resettoken)