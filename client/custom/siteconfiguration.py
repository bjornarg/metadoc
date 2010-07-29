# -*- coding: utf-8 -*-
#
#            custom/siteconfiguration.py is part of MetaDoc (Client).
#
# All of MetaDoc is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MetaDoc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MetaDoc.  If not, see <http://www.gnu.org/licenses/>.
# The API interface

import yaml

from abstract import MetaOutput
from configuration.entries import ConfigEntry

class SiteConfiguration(MetaOutput):
    def populate(self):
        """ Function to populate self.items with ConfigEntry.

        Customize this function to fit to your site.

        """
        f = open("config_setup.yaml")
        config_setup = yaml.load(f.read())
        f.close()
        for i in config_setup.keys():
            self.items.append(
                ConfigEntry(i, config_setup[i])
            )
