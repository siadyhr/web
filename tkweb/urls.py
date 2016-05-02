from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views
from django.views.generic.base import RedirectView

import tkweb.apps.calendar.views
import tkweb.apps.gallery.urls
import tkweb.apps.jubi.urls
import tkweb.apps.redirect.urls
import django.views.static
import django.views.defaults


urlpatterns = [
    # Examples:
    # url(r'^$', 'tkweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^$',
        RedirectView.as_view(url='/kalender/', permanent=False),
        name='index'),

    url(r'^om/$',
        views.flatpage, {'url': '/om/'},
        name='om'),
    url(r'^bestfu/$',
        views.flatpage, {'url': '/bestfu/'},
        name='bestfu'),
    url(r'^arrangementer/$',
        views.flatpage, {'url': '/arrangementer/'},
        name='arrangementer'),
    url(r'^kontakt/$',
        views.flatpage, {'url': '/kontakt/'},
        name='kontakt'),
    url(r'^ket/$',
        views.flatpage, {'url': '/ket/'},
        name='ket'),

    url(r'^kalender/',
        tkweb.apps.calendar.views.kalender,
        name='kalender'),

    url(r'^galleri/',
        include(tkweb.apps.gallery.urls),
        name='gallery'),

    # Note the missing trailing slash. This catches everything that start with
    # 'j' or 'J'.
    url(r'(?i)^J',
        include(tkweb.apps.jubi.urls),
        name='jubi'),

    url(r'^admin/',
        include(admin.site.urls)),

    # Temporary media (user uploaded static files)
    # serving from dev server
    url(r'^media/(?P<path>.*)$',
        django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),

    # 404 page for debugging
    url(r'^404/$',
        django.views.defaults.page_not_found, ),

    # Send the rest to the redirect app
    url('',
        include(tkweb.apps.redirect.urls), ),

]
