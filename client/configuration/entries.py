# -*- coding: utf-8 -*-
#
#            configuration/entries.py is part of MetaDoc (Client).
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
from utils import UniqueID

class ConfigEntry(metaelement.MetaElement):
    """ConfigEntry - Size of each element of hardware. """
    xml_tag_name = "config_entry"
    def __init__(self, element, volume):
        """Creates a config_entry 

        @param element: The element described. 
        @type element: String: nodes, cores, disk, swap, memory.
        @param volume: Number of metric for the element described.
        @type volume: int, String

        """
        u = UniqueID()
        self.attributes = {
            'element': element,
            'volume': volume,
            'id': u.get_id(),
        }
        super(ConfigEntry, self).__init__(ConfigEntry.xml_tag_name, self.attributes)
        self.legal_element = (
            'cores','nodes','disk','swap','memory',
            'system','type','cpu_type','theoretical_peak',
            'opsys','scheduling_system','total_temp_shared',
            'total_home_dir','addressable_mem','default_home_dir_size',
            'max_job_runtime','max_cpu_per_job','parallel_jobs',
            'serial_jobs','large_io_jobs','memory_per_node',
            'mpi_applications','openmp_applications',
            )
    def clean_element(self, element):
        """Checks that the element attribute contains an allowed value. 
        
        Raises an L{IllegalAttributeValueError} on illegal value.

        @param element: Element described.
        @type element: String
        @return: String
        
        """
        self._clean_allowed_values(element, self.legal_element, 'element', self.xml_tag_name, False)
        return element
    def clean_volume(self, volume):
        """Converts volume to string if integer, and checks that the passed 
        variable is either string or int.

        @param volume: Amount of metric for element.
        @type volume: int, String
        @return: String

        """
        if isinstance(volume, int):
            volume = "%d" % (volume)
        return volume
