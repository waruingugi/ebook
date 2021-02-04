from django.conf.urls import url
from payments import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    url(r'^$', views.index, name='index'),
    url(r'^details', views.details, name='details'),
    url(r'^success', views.success, name='success')
]
