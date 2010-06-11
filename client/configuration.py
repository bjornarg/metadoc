#
#            Configuration.py is part of MetaDoc (Client).
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
#

import metaelement
import xml.etree.ElementTree

class Configuration(metaelement.MetaElement):
    """ Registers events and packs to XML. 

    Specifies cleaning methods for attributes to make sure they conform with 
    expected values. 

    """
    def __init__(self, *args, **kwargs):
        """ Initialites the MetaElement and specifies legal values for attributes. """
        super(Configuration, self).__init__("config")
        self.legal_element_types = (ConfigEntry,)


class ConfigEntry(metaelement.MetaElement):
    def __init__(self, element, metric, volume):
        """ Creates a config_entry 
        
        param:
        element         : The element described (nodes, cores, totalDisk, etc)
        metric          : The metric used to measure element (count, MB, GB, TB)
        volume          : Number of <metric> for the element described. Can be int or str.

        """
        self.attributes = {
            'element': element,
            'metric': metric,
            'volume': volume,
        }
        super(ConfigEntry, self).__init__("config_entry", self.attributes)
        self.legal_metric = ('count', 'MB', 'GB', 'TB')
        self.legal_element = ('cores','nodes','totalDisk',
                                'usedDisk','totalSwap','usedSwap',
                                 'totalMemory','usedMemory')
    def clean_element(self, element):
        """ Checks that the element attribute contains an allowed value. """
        if not element in self.legal_element:
            raise metaelement.IllegalAttributeValueError("element", element, self.legal_element, "Configuration")
        return element
    def clean_metric(self, metric):
        """ Checks that the metric attribute contains an allowed value. """
        if not metric in self.legal_metric:
            raise metaelement.IllegalAttributeValueError("metric", metric, self.legal_metric, "Configuration")
        return metric
    def clean_volume(self, volume):
        """ Converts volume to string if integer, and checks that the passed 
        variable is either string or int.

        Allows for unicode strings.

        """
        if isinstance(volume, int):
            volume = "%d" % (volume)
        if not isinstance(volume, basestring):
            raise metaelement.IllegalAttributeTypeError("volume", type(volume), "Configuration", ['str', 'int'])
        return volume