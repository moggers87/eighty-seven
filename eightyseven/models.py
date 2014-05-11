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

from django.contrib.auth.models import Group, User
from django.db import models

from bitfield import BitField

__all__ = ["Group", "User", "PasswordStore", "PasswordRecord"]

class PasswordStore(models.Model):
    """A collection of passowrds

    `user` is the owner
    `group` is contains the users who are allowed to access this store
    `algoithm` is what was used to encrypt the records
    """
    user = models.ForeignKey(User)
    group = models.OneToOneField(Group, null=True)
    algorithm = models.CharField(default="AES-GCM-256", max_length=32, help_text="Algorithm used")
    flags = BitField(flags=("group_read_only"), default=1)

class PasswordRecord(models.Model):
    """A password (or maybe other data) that the client has encypted

    `updated` is not to be trusted - it is not tamper proof and is only there for convenience
    """
    store = models.ForeignKey(PasswordStore)
    data = models.TextField(null=True, help_text="Base64 encoded and encrypted JSON data")
    iv = models.CharField(null=True, max_length=128, help_text="Initialisation vector, base64 encoded")
    mac = models.CharField(null=True, max_length=128, help_text="Either digest provided by algorithm or separate HMAC")
    updated = models.DateTimeField(auto_now=True)
