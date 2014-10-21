from django.shortcuts import render
from django.core.urlresolvers import reverse


def index(request):
    """
    Controller for the app home page.
    """
    date_picker_options = {'display_text': 'Date',
               'name': 'date1',
               'autoclose': True,
               'format': 'MM d, yyyy',
               'start_date': '2/15/2014',
               'start_view': 'decade',
               'today_button': True,
               'initial': 'February 15, 2014'}

    google_map = {'height': '600px',
                  'width': '100%',
                  'kml_service': reverse('gizmos:get_kml'),
                  'maps_api_key': 'AIzaSyAswFfpH07XyrhFEjClWzXHwwhGzEhiYws'}
               
    context = {'date_picker_options': date_picker_options,
               'google_map': google_map}

    return render(request, 'death_star/index.html', context)

def new_page(request):
    """
    Controller for a new page.
    """

    context = {}

    return render(request, 'death_star/new_page.html', context)