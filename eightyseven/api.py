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

__all__ = ["PasswordStoreResource", "PasswordRecordResource"]

class UserAuthorization(Authorization):
    """Ignores group permissions"""
    def __init__(self, user_rel="user"):
        self.user_rel = user_rel

    def read_list(self, object_list, bundle):
        return object_list.filter(**{self.user_rel: bundle.request.user})

    def read_detail(self, object_list, bundle):
        if bundle.obj.pk is not None:
            qs = type(bundle.obj).objects.filter(**{self.user_rel: bundle.request.user})
            return qs.exists()
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

class PasswordStoreResource(ModelResource):
    records = fields.ToManyField("eightyseven.api.PasswordRecordResource", 'passwordrecord_set', full=True, null=True)
    flags = fields.DictField('flags__items')

    class Meta:
        queryset = PasswordStore.objects.all()
        authorization = UserAuthorization()
        authentication = BasicAuthentication()
        detail_allowed_methods = ["get", "put"]
        list_allowed_methods = ["get"]

class PasswordRecordResource(ModelResource):
    store = fields.ForeignKey("eightyseven.api.PasswordStoreResource", 'store', readonly=True)

    class Meta:
        queryset = PasswordRecord.objects.all()
        authorization = UserAuthorization("store__user")
        authentication = BasicAuthentication()
        detail_allowed_methods = ["get", "put"]
        list_allowed_methods = ["get"]
