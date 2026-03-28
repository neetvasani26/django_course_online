from django.contrib import admin
from .model import Question, Choice, Submission, Lesson, Course, Instructor, Learner


# ----------- Inlines -----------

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson          # ✅ Lesson has direct ForeignKey to Course
    extra = 1


# ----------- Admin Classes -----------

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('id', 'question_text', 'lesson')
    search_fields = ('question_text',)


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('id', 'lesson_name', 'course')
    search_fields = ('lesson_name',)


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]        # ✅ FIXED
    list_display = ('id', 'course_name')
    search_fields = ('course_name',)


# ----------- Register -----------

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)