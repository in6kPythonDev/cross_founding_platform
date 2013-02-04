from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

import registration.backends.default.urls as regUrls
import cross_founding_platform

from cross_founding_platform.cross_founding.forms import BackerRegistrationForm, BackerAuthenticationForm

from cross_founding_platform.cross_founding.signals import *

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^accounts/register/$',
        'registration.views.register',
        {'backend': 'registration.backends.default.DefaultBackend', 'form_class': BackerRegistrationForm},
        name='registration_register'),

    url(r'^accounts/login/$',
        'cross_founding_platform.cross_founding.views.login',
        {'authentication_form': BackerAuthenticationForm},
        name='auth_login',
    ),

    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'cross_founding_platform.cross_founding.views.password_reset_confirm',
        name='auth_password_reset_confirm'),

    url(r'^accounts/password/reset/$',
        'cross_founding_platform.cross_founding.views.password_reset',
        name='auth_password_reset_confirm'),

    url(r'^accounts/', include(regUrls)),
    url(r'^accounts/profile', 'cross_founding_platform.cross_founding.views.profile'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
)