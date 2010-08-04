# -*- coding: utf-8 -*-
#
#            events/entries.py is part of MetaDoc (Client).
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
from utils import UniqueID

class ResourceUpEntry(metaelement.MetaElement):
    """ Describes a resourceUp entry. """
    xml_tag_name = "resourceUp"

    def __init__(self, dateUp, reason=None, remarks=None):
        """Initializes the MetaElement and specifies legal values for 
        attributes.

        @param dateUp: Date the system came up
        @type dateUp: date, datetime, int, float, RFC3339 String
        @param reason: Reason for going down
        @type reason: String
        @param remarks: Any special remarks
        @type remarks: String

        """
        u = UniqueID()
        self.attributes = {
            'dateUp': dateUp,
            'id': u.get_id(),
        }
        if reason:
            self.attributes['reason'] = reason
        super(ResourceUpEntry, self).__init__(ResourceUpEntry.xml_tag_name, 
                                                self.attributes)
        
        self.legal_element_types = ()

        if remarks:
            self.text = remarks

    def clean_dateUp(self, dateUp):
        """Makes sure the date is in the correct format.
        
        Raises an L{IllegalAttributeValueError} on illegal value.

        @param dateUp: Date the system came up.
        @type dateUp: date, datetime, int, float, RFC3339 String
        @return: RFC3339 String
        
        """
        return self._clean_date(dateUp, 'dateUp', self.xml_tag_name)

class ResourceDownEntry(metaelement.MetaElement):
    """Describes a resourceDown entry. """
    xml_tag_name = "resourceDown"

    def __init__(self, reason, dateDown, dateUp, shareDown, remarks=None):
        """Initializes the MetaElement and specifies legal values for 
        attributes.
        
        @param reason: Reason for going down.
        @type reason: String
        @param dateDown: Date the system went down
        @type dateDown: date, datetime, int, float, RFC3339 String
        @param dateUp: Date the system will come/came up
        @type dateUp: date, datetime, int, float, RFC3339 String
        @param shareDown: Share (percentage) of system down
        @type shareDown: String, int, float
        @param remarks: Any special remarks
        @type remarks: String

        """
        u = UniqueID()
        self.attributes = {
            'reason': reason,
            'dateDown': dateDown,
            'dateUp': dateUp,
            'shareDown': shareDown,
            'id': u.get_id(),
        }
        super(ResourceDownEntry, self).__init__(ResourceDownEntry.xml_tag_name,
                                                self.attributes)

        self.legal_element_types = ()

        if remarks:
            self.text = remarks
    def clean_dateDown(self, dateDown):
        """Checks that dateDown is RFC3339 String or converts date, datetime,
        int or float to RFC3339 string. 
        
        Raises L{IllegalAttributeValueError} on illegal value.

        @param dateDown: Date the system went down.
        @type dateDown: date, datetime, int, float, RFC3339 String.
        @return: RFC3339 String
        
        """
        return self._clean_date(dateDown, 'dateDown', self.xml_tag_name)
    def clean_dateUp(self, dateUp):
        """Checks that dateUp is RFC3339 String or converts date, datetime,
        int or flat to RFC3339 String. 
        
        
        Raises L{IllegalAttributeValueError} on illegal value.

        @param dateUp: Date the system went down.
        @type dateUp: date, datetime, int, float, RFC3339 String.
        @return: RFC3339 String

        """
        return self._clean_date(dateUp, 'dateUp', self.xml_tag_name)
    def clean_shareDown(self, share_down):
        """Checks that shareDown is string or converts from int or float
        to string. 

        @param share_down: Share of resource that is down.
        @type share_down: int, float, String
        @return: String
        
        """
        if isinstance(share_down, int):
            share_down = "%d" % share_down
        elif isinstance(share_down, float):
            share_down = "%f" % share_down
        elif isinstance(share_down, basestring):
            pass
        else:
            raise metaelement.IllegalAttributeTypeError("shareDown", 
                        type(share_down), "Software", ['int', 'float', 'str'])
        return share_down
