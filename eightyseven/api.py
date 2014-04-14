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

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.exceptions import Unauthorized

from eightyseven.models import *

__all__ = ["PasswordStoreResource"]

class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        raise Unauthorized("Nope")

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized("Nope")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Nope")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Nope")

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Nope")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Nope")

class PasswordStoreResource(ModelResource):
    class Meta:
        queryset = PasswordStore.objects.all()
        authorization = UserAuthorization()
        authentication = Authentication() # TODO: don't deploy with this

    def get_object_list(self, request):
        qs = super(PasswordStoreResource, self).get_object_list(request)
        return qs.filter(user=request.user)
