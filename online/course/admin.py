from django.contrib import admin
from .models import Question, Choice, Submission, Lesson, Course, Instructor, Learner

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('id', 'question_text')
    search_fields = ('question_text',)


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('id', 'lesson_name')
    search_fields = ('lesson_name',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Learner)