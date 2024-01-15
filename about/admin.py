from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About, TeamMember

@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    summernote_fields = ('content',)

@admin.register(TeamMember)
class TeamMemberAdmin(SummernoteModelAdmin):
    list_display = ('name', 'role', 'about')
    search_fields = ('name', 'role')
    summernote_fields = ('bio',)
    raw_id_fields = ('about',)

    def get_image_preview(self, obj):
        return obj.image.url if obj.image else 'No image'
    get_image_preview.short_description = 'Image Preview'

    readonly_fields = ['get_image_preview',]
    fields = ('about', 'name', 'role', 'bio', 'image', 'get_image_preview')
