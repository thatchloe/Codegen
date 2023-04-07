from django.contrib import admin
from .models import Code, resettoken

# Register Codes
admin.site.register(Code)
admin.site.register(resettoken)