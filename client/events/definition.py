# -*- coding: utf-8 -*-
#
#            events/definition.py is part of MetaDoc (Client).
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

import metaelement
from custom.siteevents import SiteEvents
from events.entries import ResourceUpEntry, ResourceDownEntry

class Events(metaelement.MetaElement):
    """Register Events and pack it in XML. """
    xml_tag_name = "events"
    site_handler = SiteEvents
    url = "events"

    def __init__(self):
        """Initializes the MetaElement and specifies legal values for 
        attributes. 

        Allowed sub elements are: L{ResourceUpEntry}, L{ResourceDownEntry}.
        
        """
        super(Events, self).__init__(Events.xml_tag_name)
        self.legal_element_types = (ResourceUpEntry, ResourceDownEntry,)
