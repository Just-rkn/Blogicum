from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """CBV that displays about page on 'about.html'."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """CBV that displays rules page on 'rules.html'."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Returns a custom 404 error page for this error"""

    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Returns a custom 403 error page for this error"""

    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Returns a custom 500 error page for this error"""

    return render(request, 'pages/500.html', status=500)
