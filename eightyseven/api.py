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

from django.conf.urls import url

from tastypie import http, fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from eightyseven.models import *

__all__ = ["PasswordStoreResource", "UserResource"]

class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(pk=bundle.request.user.pk)

    def read_detail(self, object_list, bundle):
        if bundle.obj.pk is not None:
            return bundle.obj.pk == bundle.request.user.pk
        return True

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

class SingleModelResource(ModelResource):
    """Just like ModelResource, but has a /self/ url"""

    def get_detail(self, request, **kwargs):
        # Place the authenticated user's id in the get detail request
        if "pk" in kwargs and kwargs["pk"] == "self":
            kwargs["pk"] = request.user.pk
        return super(SingleModelResource, self).get_detail(request, **kwargs)

class UserResource(SingleModelResource):
    passwordstore = fields.ForeignKey("eightyseven.api.PasswordStoreResource", 'passwordstore', readonly=True)

    def __init__(self, *args, **kwargs):
        output = super(UserResource, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            getattr(self, field).readonly = True

    class Meta:
        queryset = User.objects.all()
        authorization = UserAuthorization()
        authentication = BasicAuthentication()
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        fields = ["date_joined", "email", "last_login", "username"]

class PasswordStoreResource(SingleModelResource):
    user = fields.ForeignKey("eightyseven.api.UserResource", 'user', readonly=True)

    class Meta:
        queryset = PasswordStore.objects.all()
        authorization = UserAuthorization()
        authentication = BasicAuthentication()
        detail_allowed_methods = ["get", "put"]
        list_allowed_methods = ["get"]
