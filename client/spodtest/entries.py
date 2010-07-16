import metaelement
from utils import UniqueID

class TestCaseEntry(metaelement.MetaElement):
    xml_tag_name = "testcase"
    def __init__(self, to, total_size, transfer_time, num_files, command_type, 
                    date, fileset_name=None, compression=None, 
                    compression_level=None, encryption=None):
            u = UniqueID()
            self.attributes = {
                'to': to,
                'total_size': total_size,
                'transfer_time': transfer_time,
                'num_files': num_files,
                'command_type': command_type,
                'date': date,
                'id': u.get_id()
            }
            if fileset_name is not None:
                self.attributes['fileset_name'] = fileset_name
            if compression is not None:
                self.attributes['compression'] = compression
            if compression_level is not None:
                self.attributes['compression_level'] = compression_level
            if encryption is not None:
                self.attributes['encryption'] = encryption

            super(TestCaseEntry, self).__init__(TestCaseEntry.xml_tag_name, 
                                                self.attributes)

    def clean_date(self, date):
        return self._clean_date(date, 'date', self.xml_tag_name)
