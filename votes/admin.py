from django.contrib import admin
from .models import Region, Candidate, Voter

# Register your models here.
admin.site.register(Region)
admin.site.register(Candidate)
admin.site.register(Voter)
