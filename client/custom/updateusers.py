from abstract import MetaInput

class UpdateUsers(MetaInput):
    def process(self):
        for item in self.items:
            print item.attributes
            for a in item.sub_elements:
                print a.attributes
