from MetaElement import MetaElement
import xml.etree.ElementTree

class Projects(MetaElement):
    """
    Information about projects tied to a system.
    """
    def __init__(self):
        """
        init()
        """
        MetaElement.__init__(self, "projects")
        self.element = xml.etree.ElementTree.Element(self.getName())
        self.legalStatus = ['new', 'existing', 'delete']

    def addEntry(self,
                 name,
                 gid,
                 status,
                 account_nmb,
                 valid_from,
                 valid_to = None,
                 usernames=None):
        """
        Add a project to the list of projects.

        param:
        - name of project
        - gid (Group ID)
        - status:
                - new           : add new project
                - existing      : update existing project
                - delete        : delete a project.
        - account_nmb           : Associated account-number.
        - valid_from            : The project should not be available before
                                  this date.
        - valid_to              : timeout switch. After this date, the project
                                  should be disabled.
        - usernames             : a list of usernames to associate with the
                                  project on the form ['foo', 'bar']. This only
                                  applies to new and existing projects.
        """
        if not status in self.legalStatus:
            print "Illegal status \"%s\" for project (%s). Use one of %s." % (status, name, self.legalStatus)
        entry = xml.etree.ElementTree.Element("project_entry",
                                              name=name,
                                              gid=gid,
                                              status=status,
                                              account_nmb=account_nmb,
                                              valid_from=valid_from)
        if valid_to:
            entry.set('valid_to', valid_to)
        if usernames:
            for user in usernames:
                xml.etree.ElementTree.SubElement(entry, "user_entry", username=user)
        self.element.append(entry)
