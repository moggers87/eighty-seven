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
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

class PlaceHolderAuthenticationForm(AuthenticationForm):
    """Same as auth.forms.AuthenticationForm but adds a label as the placeholder in each field"""
    def __init__(self, *args, **kwargs):
        output = super(PlaceHolderAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            label = field.label.title()
            field.widget.attrs.update({"placeholder": label})
        return output
