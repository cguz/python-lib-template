import logging

label_type_data = 'TypeData'

# TypeData class
class TypeData:
    def __init__(self, Name):
        self.id = 0
        self.Name = Name

    def store(self):
        self.find()
        if self.exist():
            g.V(self.id).property('Name', self.Name).next()
        else:
            result = g.addV(label_type_data).property('Name', self.Name).next()

            self.id = result.id

    def get_appropiate_algorithms(self):
        result = g.V().has("Name", self.Name).in_(edge_label_solveIf).toList()
        l_result = []
        for r in result:
            pos = len(l_result)
            l_result.append(Algorithm(g.V(r.id).values("Name").next()))
            l_result[pos].find(g)
        return l_result

    def get_appropiate_algorithms_str(self):
        result = g.V().has("Name", self.Name).in_(edge_label_solveIf).toList()
        l_result = []
        for r in result:
            l_result.append(g.V(r.id).values("Name").next())
        return l_result
        
    def find(self):
        search = g.V().hasLabel(label_type_data).has('Name', self.Name).toList()
        if len(search) != 0:
            for f in search:
                self.id = f.id
                self.Name = g.V(self.id).values('Name').next()

    def exist(self):
        return self.id != 0

    def remove(self):
         g.V(self.id).drop().iterate()




label_algorithms = 'Algorithms'
edge_label_solveIf = "isAppropiateToSolve"

# Algorithm class
class Algorithm:
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
            result = g.addV(label_algorithms).property(
                'Name', self.Name).property(
                'Description', self.Description).next()

            self.id = result.id

    # define the function to store the relation with the type_data
    def store_relation_type_data(self, type_data):

        for t in type_data:

            # if there is not a relationship between the Algorithm -> TypeData
            if not self.exist_relation_type_data(t.Name):
                
                # create the relation
                g.V(t.id).as_('t').V(self.id).addE(edge_label_solveIf).to('t').next()
                
                logging.info("[Relation Created] ", self.Name, "- (", edge_label_solveIf, ") >", t.Name)

            else:
                logging.info("[Relation Exist] ", self.Name, "->", t.Name)

    def exist_relation_type_data(self, name):
        return self.exist_relationship(name, edge_label_solveIf)

    def exist_relationship(self, name, edge_label):
        
        # search for the relationship
        search = g.V().has("Name", self.Name).outE(edge_label).inV().has("Name", name).toList()
        if len(search) != 0:
            return True
        return False          

    def find(self):
        search = g.V().hasLabel(label_algorithms).has('Name', self.Name).toList()
        if len(search) != 0:
            for f in search:
                self.id = f.id
                self.Name = g.V(self.id).values('Name').next()
                self.Description = g.V(self.id).values('Description').next()

    def exist(self):
        return self.id != 0

    def remove(self):
         g.V(self.id).drop().iterate()