from django.contrib import admin
from .models import *


admin.site.register(Category)


class OfferAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'price', 'delivery_time')
admin.site.register(Offer, OfferAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'publish_date', 'budget', 'location')
admin.site.register(Project, ProjectAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'location')
admin.site.register(Profile, ProfileAdmin)
