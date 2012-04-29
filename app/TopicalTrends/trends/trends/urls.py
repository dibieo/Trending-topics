from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^ui/$', 'ui.views.index'),
    url(r'^ui/topics$', 'ui.views.topics')
)
