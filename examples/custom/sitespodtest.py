from abstract import MetaOutput
from spodtest.entries import TestCaseEntry
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
import os

class SiteSPODTest(MetaOutput):
    def populate(self):
        """Populates I{self.items} with L{TestCaseEntry} instances.

        Example that parses a SPODTest XML data file and creates 
        L{TestCaseEntry} instances for each test case.

        Please change I{SPODTEST_FILE} to the location of your SPODTest data.

        """
        SPODTEST_FILE = "/tml/xmldoc.xml"
        try:
            xmldoc = open(SPODTEST_FILE, 'r')
        except:
            return
        xml = etree.parse(xmldoc)
        testcases = xml.findall('testcase')
        for tc in testcases:
            tca = tc.attrib
            self.items.append(TestCaseEntry(
                    to=tca.get('to'),
                    total_size=tca.get('total_size'),
                    transfer_time=tca.get('transfer_time'),
                    num_files=tca.get('num_files'),
                    command_type=tca.get('type'),
                    date=tca.get('date'),
                    fileset_name=tca.get('fileset_name', None),
                    compression=tca.get('compression', None),
                    compression_level=tca.get('compression_level', None),
                    encryption=tca.get('encryption', None),
                    fileset=tca.get("fileset", None),
                ))
        os.remove('/tmp/xmldoc.xml')
