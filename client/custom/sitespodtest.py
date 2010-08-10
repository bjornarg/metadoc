from abstract import MetaOutput
from spodtest.entries import TestCaseEntry
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
import os

class SiteSPODTest(MetaOutput):
    def populate(self):
        """Should populate I{self.items} with L{TestCaseEntry} instances.

        Customize this to fit your site.

        """
        pass
