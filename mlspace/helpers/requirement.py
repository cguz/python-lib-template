from mlspace.helpers.functions import g 

label_requirement = "Requirement"
label_arguments = "Arguments"

edge_label_contains = "contains"

class Requirement:
    """
    Class that represents the requirements on the Ontology

    Arguments
    ----------
    id : str 
        identificator of the requirement 
    name : str 
        name of the requirement 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    arguments : DataFrame 
        set of arguments required for the QGs
    """
    def __init__(self, Name, ArgsName = [], ArgsValue = []):
        self.id = 0
        self.Name = Name
        self.ArgumentsName = ArgsName
        self.ArgumentsValue = ArgsValue

    def find(self):
        search = g.V().hasLabel(label_requirement).has('Name', self.Name).toList()
        if len(search) != 0:
            for f in search:
                self.id = f.id
                self.fill()

    def fill(self):
        self.Name = g.V(self.id).values('Name').next()
        self.ArgumentsName = []
        self.ArgumentsValue = []
        
        # For the arguments need to iterate to node's edge
        search = g.V(self.id).outE(edge_label_contains).inV().toList()
        for arg in search:
            name = g.V(arg).values("Name").next()
            value = g.V(arg).values("Value").next()
            try:
                check = isinstance(value, int)
                if check:
                    value = int(value)
                else:
                    check = isinstance(value, float)
                    if check:
                        value = float(value)
            except ValueError:
                try: 
                    value = float(value)
                except ValueError:
                    value = value
            self.ArgumentsName.append(name)
            self.ArgumentsValue.append(value)

    def exist_relationship(self, name, edge_label):
        
        # search for the relationship
        search = g.V().has("Name", self.Name).outE(edge_label).inV().has("Name", name).toList()
        if len(search) != 0:
            return True
        return False

    def exist_relationship_by_id(self, name, edge_label):    
            
        # search for the relationship
        search = g.V(self.id).outE(edge_label).inV().has("Name", name).toList()
        if len(search) != 0:
            return True
        return False

    def exist(self):
        return self.id != 0

    def remove(self):
        self.g.V(id).drop().iterate()