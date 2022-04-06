import logging

label_expe_distribution = "ExpectedDistribution"

class ExpectedDistribution:

    def __init__(self, Name, Hist = '', Bins = '', Ppf = '', Cdf = ''):
        self.id = 0
        self.Name = Name
        self.Hist = Hist
        self.Bins = Bins
        self.Ppf  = Ppf
        self.Cdf  = Cdf

    def store(self):
        self.find()

        if self.exist():
            g.V(self.id).property('Name', self.Name).next()
            g.V(self.id).property('Hist', self.Hist).next()
            g.V(self.id).property('Bins', self.Bins).next()
            g.V(self.id).property('Ppf', self.Ppf).next()
            g.V(self.id).property('Cdf', self.Cdf).next()
        else:
            result = self.g.addV(label_expe_distribution).property(
                'Name', self.Name).property(
                'Hist', self.Hist).property(
                'Bins', self.Bins).property(
                'Ppf', self.Ppf).property(
                'Cdf', self.Cdf).next()
            self.id = result.id
            logging.info(self.id)
            logging.info(self.Name)
            logging.info("Hist: ", len(self.Hist))
            logging.info("Bins: ", len(self.Bins))
            logging.info("Ppf: ", len(self.Ppf))
            logging.info("Cdf: ", len(self.Cdf))

    def find(self):
        search = self.g.V().hasLabel(label_expe_distribution).has('Name', self.Name).toList()
        if len(search) != 0:
            for f in search:
                self.id = f.id
                self.fill()

    def fill(self):
        self.Name = self.g.V(self.id).values('Name').next()
        if len(self.Hist) == 0:
            self.Hist = self.g.V(self.id).values('Hist').next()
        if len(self.Bins) == 0:
            self.Bins = self.g.V(self.id).values('Bins').next()
        if len(self.Ppf) == 0:
            self.Ppf  = self.g.V(self.id).values('Ppf').next()
        if len(self.Cdf) == 0:
            self.Cdf  = self.g.V(self.id).values('Cdf').next()

    def exist(self):
        return self.id != 0

    def remove(self):
        self.g.V(self.id).drop().iterate()