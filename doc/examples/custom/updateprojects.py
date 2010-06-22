# -*- coding: utf-8 -*-
#
#            custom/updateprojects.py is part of MetaDoc (Client).
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

from abstract import MetaInput

import datetime

class UpdateProjects(MetaInput):
    def process(self):
        """ Processes any project data recieved. 
        
        Example that creates a file listing usernames per project.
        
        """
        projects_file = open("/tmp/users.%s" % 
            datetime.datetime.now().strftime("%Y-%m-%d"), "w")
        for item in self.items:
            print item.attributes
            for project in item.sub_elements:
                line = "%s:" % project.attributes.get("account_nmb")
                users = project.get_user_list()
                for user in users:
                    line += "%s," % user.attributes.get("username")
                line = line[:-1]
                if len(users) > 0:
                    projects_file.write("%s\n" % line)
        projects_file.close()
