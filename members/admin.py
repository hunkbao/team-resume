from django.contrib import admin
from .models import Profile, Course, FavoriteWebsite


class CourseInline(admin.TabularInline):
    model = Course
    extra = 1


class WebsiteInline(admin.TabularInline):
    model = FavoriteWebsite
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'political_status', 'verify_course', 'updated_at']
    list_filter = ['political_status', 'grade']
    search_fields = ['name', 'hometown']
    inlines = [CourseInline, WebsiteInline]
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'birth_date', 'ethnicity', 'hometown',
                       'political_status', 'grade', 'photo')
        }),
        ('联系方式', {
            'fields': ('email', 'wechat', 'qq')
        }),
        ('个人介绍', {
            'fields': ('specialties', 'hobbies', 'future_plan')
        }),
        ('验证设置', {
            'fields': ('verify_course',),
            'description': '设置用于登录验证的课程名称'
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'profile', 'semester']
    search_fields = ['name']


@admin.register(FavoriteWebsite)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'profile', 'url']
    search_fields = ['title']
