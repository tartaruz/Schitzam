from model.case import case
import math
import random

class Retrieval:
    def __init__(self, DB):
        self.DB = DB
        self.cases = self.retiveCases()
        self.queryCase = None
        self.similarCases = None
        self.retrievedCases = None

    def euclidian_distance(self,v1, v2):
        summation =  0
        for i in range(len(v1)):
            summation += math.pow(v1[i] - v2[i], 2)
        return math.sqrt(summation)

    def knn(self, K):
        distances = {}
        casesValues = [c.returnNumericValue() for c in self.cases]
        for i in range(len(casesValues)):
            d = self.euclidian_distance(casesValues[i], self.queryCase.returnNumericValue())
            distances[i] = d
        
        # Selecting the K nearest neighbors
        k_neighbors = [[key, value] for key, value in sorted(distances.items(), key=lambda case: case[1])][:K]
        self.similarCases = [[self.cases[index[0]].track_id,index[1]] for index in k_neighbors]
        self.retrievedCases = [list(filter(lambda x: x.track_id == track_id, self.cases))[0] for track_id in map(lambda x: x[0], self.similarCases)]
    
    def retiveCases(self):
        self.DB.cursor.execute("SELECT * FROM cases")
        result = self.DB.cursor.fetchall()
        return [case(data) for data in result]

