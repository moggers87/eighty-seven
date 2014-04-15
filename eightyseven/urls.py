##
#    Copyright (C) 2014 Matt Molyneaux
#
#    This file is part of Eighty Seven.
#
#    Eighty Seven is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Eighty Seven is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Eighty Seven.  If not, see <http://www.gnu.org/licenses/>.
##

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from tastypie.api import Api

from eightyseven.api import *
from eightyseven.forms import PlaceHolderAuthenticationForm
from eightyseven.views import *

_login_context = { # extra context for contrib.auth views
                    "site_name": settings.SITE_NAME,
                    "enable_registration": settings.ENABLE_REGISTRATION,
                    "headline": _("Login"),
                }

api_v1 = Api(api_name="v1")
api_v1.register(PasswordStoreResource())
api_v1.register(UserResource())

urlpatterns = patterns('',
    url(r'^$', StaticView.as_view(template_name="index.html", headline=_("Welcome")), name="index"),
    url(r'^api/', include(api_v1.urls)),
    url(r'^home/$', HomeView.as_view(), name="home"),
    url(r'^login/$', "django.contrib.auth.views.login", {"template_name": "login.html", "authentication_form": PlaceHolderAuthenticationForm, "extra_context": _login_context}, name="login"),
    url(r'^logout/$', "django.contrib.auth.views.logout", {"next_page": reverse_lazy("index")}, name="logout"),
    url(r'^$', StaticView.as_view(template_name="index.html", headline=_("Fake signup page")), name="signup"),
    )
