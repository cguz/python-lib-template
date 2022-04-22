
from mlspace.helpers.functions import g 

label_fill_gap = 'FillGaps'

# FillGaps classes
class FillGaps:
    def __init__(self, Name, Description=''):
        self.id = 0
        self.Name = Name
        self.Description = Description

    def store(self):
        self.find()
        if self.exist():
            g.V(self.id).property('Name', self.Name).next()
            g.V(self.id).property('Description', self.Description).next()
        else:
            result = g.addV(label_fill_gap).property(
                'Name', self.Name).property(
                'Description', self.Description).next()

            self.id = result.id

    def find(self):
        # time.sleep(0.5)
        search = g.V().hasLabel(label_fill_gap).has('Name', self.Name).toList()
        if len(search) != 0:
            for f in search:
                self.id = f.id
                self.Name = g.V(self.id).values('Name').next()
                self.Description = g.V(self.id).values('Description').next()

    def exist(self):
        return self.id != 0

    def remove(self):
        g.V(self.id).drop().iterate()