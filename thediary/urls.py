from django.conf.urls import patterns, include, url

from django.contrib import admin
from thediary.views import index
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thediary.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index)
)
