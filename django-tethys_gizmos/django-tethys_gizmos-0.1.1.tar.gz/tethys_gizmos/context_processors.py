from django.conf import settings

def tethys_gizmos_context(request):
    """
    Add the gizmos_rendered context to the global context.
    """
    # Extract keys from settings file if present
    google_maps_key = ''

    if hasattr(settings, 'TETHYS_GIZMOS_GOOGLE_MAPS_API_KEY'):
        google_maps_key = settings.TETHYS_GIZMOS_GOOGLE_MAPS_API_KEY

    # Setup variables
    context = {'gizmos_rendered': [],
               'gizmos_google_maps_key': google_maps_key}
    return context