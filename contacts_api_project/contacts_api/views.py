from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page offering navigation to authentication and contacts."""
    template_name = 'home.html'
