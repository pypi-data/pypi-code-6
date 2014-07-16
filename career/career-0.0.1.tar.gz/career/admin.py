from django.contrib import admin
from hvad.admin import TranslatableAdmin

from webapp.models import Question, Quiz, Student, Career, Teacher, QuizToCareer

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3

class QuizToCareerInline(admin.StackedInline):
    model = QuizToCareer
    extra = 3

class QuizAdmin(TranslatableAdmin):
    inlines = [QuestionInline]
    
class CareerAdmin(admin.ModelAdmin):
    inlines = [QuizToCareerInline]


admin.site.register(Career, CareerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
