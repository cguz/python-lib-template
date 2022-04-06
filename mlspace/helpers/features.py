from mlspace.helpers.requirement import Requirement
from mlspace.helpers.expected_distribution import ExpectedDistribution

import logging

label_feature = 'Feature'
label_expe_distribution = "ExpectedDistribution"
label_requirement = "Requirement"
label_arguments = "Arguments"

edge_label_is_related = "isRelated"
edge_label_hasA = "hasA"
edge_label_contains = "contains"

# Feature and Features classes
class Feature:
    def __init__(self, Name, TypeData='', TypeFeature='', Relationship='', MinValue='0.0', MaxValue='0.0'):
        self.id = 0
        self.Name = Name
        self.TypeData = TypeData
        self.TypeFeature = TypeFeature
        self.MaxValue = MaxValue
        self.MinValue = MinValue
        self.Relationship = Relationship

    def store(self):
        self.find()
        if self.exist():
            g.V(self.id).property('Name', self.Name).next()
            g.V(self.id).property('TypeData', self.TypeData).next()
            g.V(self.id).property('TypeFeature', self.TypeFeature).next()
            g.V(self.id).property('MaxValue', self.MaxValue).next()
            g.V(self.id).property('MinValue', self.MinValue).next()
            g.V(self.id).property('Relationship', ' '.join(self.Relationship)).next()
        else:
            result = g.addV(label_feature).property(
                'Name', self.Name).property(
                'TypeData', self.TypeData).property(
                'TypeFeature', self.TypeFeature).property(
                'MaxValue', self.MaxValue).property(
                'MinValue', self.MinValue).property(
                'Relationship', ' '.join(self.Relationship)).next()

            self.id = result.id

    def store_relationship(self):

        for r in self.Relationship:
            if len(r) != 0:
                if not self.exist_relationship(r, edge_label_is_related):

                    logging.info("creating relationship: ", self.Name, " (", self.id, ") ", edge_label_is_related, " ", r)
                    
                    # create the relationship  self.id -> feature.id with the edge_label_is_related
                    g.V().has('Name', r).as_('t').V(self.id).addE(edge_label_is_related).to('t').next()


    # define the function to store the requirements or constraints to be used in the expectations
    def store_requirements(self, requirements):

        # for each Requirement
        for constraint in requirements:

            # if there is not a relationship between the Feature -> Requirement
            logging.info('check if relationship {0} - ({1}) -> {2} exist'.format(self.Name, edge_label_hasA, constraint.Name))
            if not self.exist_relationship(constraint.Name, edge_label_hasA):
                logging.info(" - does not exist")
                
                # create the Requirement
                logging.info(' - add vertice {0} with Name = {1} '.format(label_requirement, constraint.Name))
                result_req_dist = g.addV(label_requirement).property("Name", constraint.Name).next()
                            
                # create the relationship Feature - hasA > Requirement
                logging.info(" - create relationship {0} - ({1}) -> {2}".format(self.Name, edge_label_hasA, constraint.Name))
                g.V(result_req_dist.id).as_('t').V(self.id).addE(edge_label_hasA).to('t').next()

            else:
                logging.info(" - relationship exists")

                # since we have a relationship with Requirement, we get the Requirement 
                logging.info(" - search all nodes with the criterium Feature -(hasA)-> Requirement: {0} - ({1}) -> {2}".format(self.Name, edge_label_hasA, constraint.Name))
                result_req_dist = g.V(self.id).outE(edge_label_hasA).inV().has("Name", constraint.Name).toList()
                    
                logging.info(" - found: {0}".format(str(result_req_dist)))

            # assign the id to the constraint
            len_results = len(result_req_dist)
            if len_results > 0:
                constraint.id = result_req_dist[len_results-1].id
            else:
                constraint.id = result_req_dist.id

            # we add repeating arguments
            # I think it is not important to control it
            # for each requirement, we add the argument
            for index in range (len(constraint.ArgumentsName)):

                arg = constraint.ArgumentsName[index]

                logging.info("check if relationship by id {0} - ({1}) -> {2}".format(constraint.Name, edge_label_contains, arg))
                if not constraint.exist_relationship_by_id(arg, edge_label_contains):
                    
                    logging.info(" - does not exist")

                    # create the argument
                    logging.info(" - add vertice {0} with Name = {1} and Value = {2}".format(label_arguments, arg, str(constraint.ArgumentsValue[index])))
                    result_argument = g.addV(label_arguments).property("Name", arg).property("Value", constraint.ArgumentsValue[index]).next()

                    # create the relationship Requirement - (contains) -> Arguments
                    logging.info(" - create relationship {0} - ({1}) -> {2}".format(arg, edge_label_contains, constraint.Name))
                    g.V(result_argument.id).as_('t').V(constraint.id).addE(edge_label_contains).to('t').next()
                else:
                    logging.info(" - relationship exists")

                    # since the relationship exists, we get the Arguments
                    logging.info(" - search all nodes with the criterium Requirement -(contains)-> Argument : {0} - ({1}) -> {2} ".format(constraint.Name, edge_label_contains, arg))                    
                    result_argument = g.V(constraint.id).outE(edge_label_contains).inV().has("Name", arg).toList()

                    logging.info(result_argument)
                    
                    g.V(result_argument[len(result_argument)-1].id).property('Value', constraint.ArgumentsValue[index]).next()


    # define the function to store the expected distribution
    def store_expected_distribution(self, expe_dist):

        # we store the expected distribution
        expe_dist.store()

        # if there is not a relationship between the feature -> ExpectedDistribution
        if not self.exist_relationship(expe_dist.Name, edge_label_hasA):

            # create the relationship Feature - hasA > ExpectedDistribution
            g.V(expe_dist.id).as_('t').V(self.id).addE(edge_label_hasA).to('t').next()

            logging.info("[Relationship Created] ", self.Name, "- (", edge_label_hasA, ") >", expe_dist.Name)

        else:
            logging.info("[Relationship Exist] ", self.Name, "->", expe_dist.Name)

    def exist_relationship(self, name, edge_label):
        
        # search for the relationship
        search = g.V().has("Name", self.Name).outE(edge_label).inV().has("Name", name).toList()
        if len(search) != 0:
            return True
        return False

    def find(self):
        # time.sleep(0.5)
        search = g.V().hasLabel(label_feature).has('Name', self.Name).toList()
        if len(search) != 0:
            for f in search:
                self.id = f.id
                self.TypeData = g.V(f.id).values('TypeData').next()
                self.TypeFeature = g.V(f.id).values('TypeFeature').next()
                self.MaxValue = g.V(f.id).values('MaxValue').next()
                self.MinValue = g.V(f.id).values('MinValue').next()
                self.Relationship = g.V(f.id).values('Relationship').next().split(" ")

    def get_requirements(self, name_requirement):

        constraint = []

        # if there is a relationship between the Feature -> Requirement    
        if self.exist_relationship(name_requirement, edge_label_hasA):

            # add the Expectation
            result_req_dist = self.get_requirement_relationship(name_requirement)

            constraint = Requirement(name_requirement)
            constraint.id = result_req_dist[len(result_req_dist)-1].id

            # print ("Requirement Arguments Name: ", constraint.ArgumentsName)
            # print ("Requirement Arguments Value: ", constraint.ArgumentsValue)

            constraint.fill()

        return constraint

    def get_requirement_relationship(self, name_requirement):
        return g.V().hasLabel(label_feature).has("Name", self.Name).outE(edge_label_hasA).inV().has("Name", name_requirement).toList()
               
    def get_expected_distribution(self, name_exp_dist):

        # if there exists a relationship between the Feature -> ExpectedDistribution
        if self.exist_relationship(name_exp_dist, edge_label_hasA):
            exp_dist = ExpectedDistribution(name_exp_dist)
            exp_dist.find()

        return exp_dist

    def exist(self):
        return self.id != 0

    def remove(self):
        g.V(self.id).drop().iterate()

    

class Features:
    def __init__(self, Features):
        self.Features = Features