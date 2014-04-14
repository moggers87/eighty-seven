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

from django.contrib.auth.models import User
from django.db import models

from annoying.fields import AutoOneToOneField

__all__ = ["PasswordStore", "User"]

class PasswordStore(models.Model):
    """Nothing more than a key-value store with a bit of meta data

    `data` is expected to be base64 encoded as most, if not all, of our
    transports will require base64 data anyway

    `algorithm`, `iv`, `mode` are provided to allow upgrades later on
    """
    user = AutoOneToOneField(User, primary_key=True)
    data = models.TextField(null=True, help_text="Base64 encoded and encrypted JSON data")
    iv = models.CharField(null=True, max_length=32, help_text="Initialisation vector, base64 encoded")
    algorithm = models.CharField(default="AES-256", max_length=32, help_text="Algorithm used")
    mode = models.CharField(default="CBC", max_length=32, help_text="Block cipher mode used")
