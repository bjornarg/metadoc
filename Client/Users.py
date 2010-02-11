from MetaElement import MetaElement
import xml.etree.ElementTree

class Users(MetaElement):
    """
    List of users tied to a system.
    """
    def __init__(self):
        """
        """
        MetaElement.__init__(self, "users")
        self.element = xml.etree.ElementTree.Element(self.getName())
        self.legalStatus = ['new', 'existing', 'delete']

    def addEntry(self,
                 username,
                 full_name=None,
                 uid=None,
                 password=None,
                 default_group=None,
                 special_path=None,
                 shell=None,
                 email=None,
                 phone=None,
                 status=None):
        """
        Add a user to the system.

        param:
        - username              : username of the person
        - full_name             : The full name of the person
        - uid                   : User ID at the system.
        - password              : initial password
        - default_group         : initial group
        - special_path          : if the home-share should be located elsewhere
                                  than /home/username
        - shell                 : the shell for the user
        - email                 : email
        - phone                 : contact phone
        - status
                - new           : add new user
                - existing      : update existing user with new vals
                - delete        : delete the user.
        """
        userEntry = xml.etree.ElementTree.Element("user_entry",
                                                  username=username)
        if full_name:
            userEntry.set('full_name', full_name)
        if uid:
            userEntry.set('uid', uid)
        if password:
            userEntry.set('password', password)
        if default_group:
            userEntry.set('default_group',default_group)
        if special_path:
            userEntry.set('special_path',special_path)
        if shell:
            userEntry.set('shell',shell)
        if email:
            userEntry.set('email',email)
        if phone:
            userEntry.set('phone',phone)
        if status:
            if status in self.legalStatus:
                userEntry.set('status',status)
            else:
                print "Illegal status \"%s\" for entry (%s). Use one of %s" % (status, username, self.legalStatus)
                userEntry = None
                return
        self.element.append(userEntry)