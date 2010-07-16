from abstract import MetaOutput
from spodtest.entries import TestCaseEntry
from lxml import etree

class SiteSPODTest(MetaOutput):
    def populate(self):
        xmldoc = open('/tmp/xmldoc.xml', 'r')
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
                ))
