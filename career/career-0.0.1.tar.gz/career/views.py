# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404

from webapp.models import Student, Teacher, Quiz, Question, Career
from webapp.forms import StudentForm, TeacherForm, QuizForm, QuestionForm, CareerForm


def home(request):
    context = []
    if request.user.is_authenticated():
        context = {
        }
        return render(request, 'webapp/home.html', context)
    

@login_required
def student_view(request, pk=None):
    if pk is None:
        students = Student.objects.all()
        context = {
            'students': students
        }
        return render(request, 'webapp/student_list_view.html', context)
    else:
        student = Student.objects.get(pk=pk)
        context = {
            'student': student
        }
        return render(request, 'webapp/student_view.html', context)

@user_passes_test(lambda u: u.is_superuser)
def student_delete(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()

    return redirect('student_view')

@user_passes_test(lambda u: u.is_superuser)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form
    }
    return render(request, 'webapp/student_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('student_view')

    context = {
        'form': form
    }
    return render(request, 'webapp/student_edit.html', context)

@login_required
def teacher_view(request, pk=None):
    if pk is None:
        teachers = Teacher.objects.all()
        context = {
            'teachers': teachers
        }
        return render(request, 'webapp/teacher_list_view.html', context)
    else:
        teacher = Teacher.objects.get(pk=pk)
        context = {
            'teacher': teacher
        }
        return render(request, 'webapp/teacher_view.html', context)

@user_passes_test(lambda u: u.is_superuser)
def teacher_delete(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    teacher.delete()

    return redirect('teacher_view')

@user_passes_test(lambda u: u.is_superuser)
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
    else:
        form = TeacherForm(instance=teacher)

    context = {
        'form': form
    }
    return render(request, 'webapp/teacher_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def teacher_add(request):
    form = TeacherForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('teacher_view')

    context = {
        'form': form
    }
    return render(request, 'webapp/teacher_edit.html', context)

@login_required
def quiz_view(request, pk=None):
    if pk is None:
        quizzes = Quiz.objects.all()
        context = {
            'quizzes': quizzes
        }
        return render(request, 'webapp/quiz_list_view.html', context)
    else:
        quiz = Quiz.objects.get(pk=pk)
        context = {
            'quiz': quiz
        }
        return render(request, 'webapp/quiz_view.html', context)

@user_passes_test(lambda u: u.is_superuser)
def quiz_delete(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    quiz.delete()

    return redirect('quiz_view')

@user_passes_test(lambda u: u.is_superuser)
def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
    else:
        form = QuizForm(instance=quiz)

    context = {
        'form': form
    }
    return render(request, 'webapp/quiz_edit.html', context)

@login_required
def quiz_add_question(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_view', pk=quiz.id)

    else:
        form = QuestionForm(initial={ 'quiz' : quiz})
    
    context = {
        'form': form
    }
    return render(request, 'webapp/quiz_add_question.html', context)

@user_passes_test(lambda u: u.is_superuser)
def quiz_add(request):
    form = QuizForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('quiz_view')

    context = {
        'form': form
    }
    return render(request, 'webapp/quiz_edit.html', context)

@login_required
def career_view(request, pk=None):
    if pk is None:
        careers = Career.objects.all()
        context = {
            'careers': careers
        }
        return render(request, 'webapp/career_list_view.html', context)
    else:
        career = Career.objects.get(pk=pk)
        context = {
            'career': career
        }
        return render(request, 'webapp/career_view.html', context)

@user_passes_test(lambda u: u.is_superuser)
def career_delete(request, pk):
    career = Career.objects.get(pk=pk)
    career.delete()

    return redirect('career_view')

@user_passes_test(lambda u: u.is_superuser)
def career_edit(request, pk):
    career = get_object_or_404(Career, pk=pk)
    if request.method == 'POST':
        form = CareerForm(request.POST, instance=career)
        if form.is_valid():
            form.save()
    else:
        form = CareerForm(instance=career)

    context = {
        'form': form
    }
    return render(request, 'webapp/career_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def career_add(request):
    form = CareerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('career_view')

    context = {
        'form': form
    }
    return render(request, 'webapp/career_edit.html', context)
