import metaelement
from custom.sitespodtest import SiteSPODTest
from spodtest.entries import TestCaseEntry

class SPODTest(metaelement.MetaElement):
    xml_tag_name = "spodtest"
    site_handler = SiteSPODTest
    url = "spodtest"

    def __init__(self):
        """Defines the spodtest element """
        super(SPODTest, self).__init__(SPODTest.xml_tag_name)
        self.legal_element_types = (TestCaseEntry,)
