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
from django.views.generic import TemplateView, DetailView

from braces.views import LoginRequiredMixin, SetHeadlineMixin, StaticContextMixin

from eightyseven.models import *

class CommonMixin(SetHeadlineMixin, StaticContextMixin):
    """Common items that are used in all views

    Can be given headline (string) and static_context (dict)
    """
    static_context = {"site_name": settings.SITE_NAME, "enable_registration": settings.ENABLE_REGISTRATION}

class StaticView(CommonMixin, TemplateView):
    """TemplateView, with CommonMixin"""
    pass

class HomeView(LoginRequiredMixin, CommonMixin, DetailView):
    """Home view for logged in user, gives them their encrypted blob"""
    headline = _("Home")
    model = PasswordStore
    template = "passwordstore.html"

    def get_object(self):
        obj =  self.model.get(user=self.request.user)
