from django.shortcuts import redirect, render


def home(request):
    return render(request, 'pml/tests/home.html')


def banner(request):
    return render(request, 'pml/tests/banner.html')


def go_back(request):
    return redirect('/')
