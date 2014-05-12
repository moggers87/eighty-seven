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

class UserAuth(Authorization):
    """Ignores group permissions"""
    user_rel = "user"

    def __getattr__(self, name):
        try:
            auth_type = name.split("_")[1]
        except IndexError:
            raise AttributeError("No such method: {0}".format(name))

        return getattr(self, "default_{0}".format(auth_type))

    def get_user_attr(self, obj):
        """Grabs the user field from obj, using self.user_rel to find it"""
        return reduce(getattr, self.user_rel, obj)

    def default_detail(self, object_list, bundle):
        return self.get_user_attr(bundle.obj) == bundle.request.user

    def default_list(self, object_list, bundle):
        raise Unauthorized("Nope")

    def read_list(self, object_list, bundle):
        return object_list.filter(**{self.user_rel: bundle.request.user})

    def read_detail(self, object_list, bundle):
        if bundle.obj.pk is not None:
            qs = type(bundle.obj).objects.filter(**{self.user_rel: bundle.request.user})
            return qs.exists()
        return True

class RecordUserAuth(UserAuth):
    user_rel = "store__user"

class PasswordStoreResource(ModelResource):
    records = fields.ToManyField("eightyseven.api.PasswordRecordResource", 'passwordrecord_set', full=True, null=True)
    flags = fields.DictField('flags__items', readonly=True)

    class Meta:
        queryset = PasswordStore.objects.all()
        authorization = UserAuth()
        authentication = BasicAuthentication()
        excludes = ["group"]

    def obj_create(self, bundle, **kwargs):
        kwargs["user"] = bundle.request.user
        return super(PasswordStoreResource, self).obj_create(bundle, **kwargs)

class PasswordRecordResource(ModelResource):
    store = fields.ForeignKey("eightyseven.api.PasswordStoreResource", 'store')
    updated = fields.DateTimeField("updated", readonly=True)

    class Meta:
        queryset = PasswordRecord.objects.all()
        authorization = RecordUserAuth()
        authentication = BasicAuthentication()
