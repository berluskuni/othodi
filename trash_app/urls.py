__author__ = 'berluskuni'
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='trasher/order.html'), name='trash_index')
]
