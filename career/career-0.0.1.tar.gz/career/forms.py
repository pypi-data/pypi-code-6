# -*- coding: utf-8 -*-
from django import forms

from webapp.models import Student, Teacher, Quiz, Question, Career

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question

class CareerForm(forms.ModelForm):
    class Meta:
        model = Career 
