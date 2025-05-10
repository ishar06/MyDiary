from django.contrib import admin
from .models import DiaryEntry, UserProfile

@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'mood', 'created_at', 'updated_at')
    list_filter = ('mood', 'created_at', 'user')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'age', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__username', 'phone_number', 'address')
