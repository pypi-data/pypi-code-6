from django.shortcuts import render


def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'this_is_an_app_with_a_very_very_long_name/home.html', context)