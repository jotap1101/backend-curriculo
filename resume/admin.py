from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(AreaOfInterest)
class AreaOfInterestAdmin(admin.ModelAdmin):
    class SubareaOfInterestInline(admin.StackedInline):
        model = SubareaOfInterest
        extra = 0

    inlines = [SubareaOfInterestInline]

@admin.register(SubareaOfInterest)
class SubareaOfInterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(StatusResume)
class StatusResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    class EducationInline(admin.StackedInline):
        model = Education
        extra = 0

    class ExperienceInline(admin.StackedInline):
        model = Experience
        extra = 0

    class LanguageInline(admin.TabularInline):
        model = ResumeLanguage
        extra = 0

    filter_horizontal = ['subareas_of_interest', 'skills']
    inlines = [EducationInline, ExperienceInline, LanguageInline]
    list_display = ['id']

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(LanguageLevel)
class LanguageLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ResumeLanguage)
class ResumeLanguageAdmin(admin.ModelAdmin):
    list_display = ['id']