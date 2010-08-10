# -*- coding: utf-8 -*-
#
#            custom/sitesoftware.py is part of MetaDoc (Client).
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

import subprocess

from abstract import MetaOutput
from software.entries import SoftwareEntry

class SiteSoftware(MetaOutput):
    def populate(self):
        """Function to populate I{self.items} with L{SoftwareEntry}.

        Uses the C{module} command to list installed modules. Parses 
        this list and uses them as installed 

        """
        MODULES_PATH = "/usr/local/Modules/3.2.6/bin/modulecmd"
        p = subprocess.Popen('%s bash avail -l' % MODULES_PATH, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE, 
            shell=True)
        ret = p.communicate()
        parts = []
        programs = {}
        for se in ret:
                if len(se) < 1:
                        continue
                parts.extend(se.split("\n"))
        
        for part in parts:
                ps = part.split()
                if len(ps) < 3 or len(ps) > 4:
                        continue
                prog_parts = ps[0].split("/")
                if prog_parts[0] not in programs.keys():
                        programs[prog_parts[0]] = set()
                programs[prog_parts[0]].add("/".join(prog_parts[1:]))
        for program in programs:
            for version in programs[program]:
                self.items.append(SoftwareEntry(program, version))

