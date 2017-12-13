import numpy as np
import copy
import random

multSigmoid = 0.01

def m_sum(m):
    val=0
    for i in range(0, len(m)):
        val+=m[i]
    return val


def m_sub(m1, m2):
    if(len(m1)==len(m2)):
        tempArray=[]
        for i in range(0, len(m1)):
            tempArray.append(m1[i]-m2[i])
        return tempArray

def m_pow(m1, m2):
    tempArray=[]
    for i in range(0, len(m1)):
        tempArray.append(pow(m1[i], m2))
    return tempArray


def sigmoid(z):
    return 1.0/(1+np.exp(-multSigmoid*z))

def sigmoidArray(z):
    tempVar = []
    for i in range(0, len(z)):
        tempVar.append(sigmoid(z[i]))
    return tempVar

def inverseSigmoid(z):
    if z != 1:
        return (1.0/multSigmoid)*np.ln(z/(1-z))
    return "DNE"

def getMaxIndex(array):
    k = 0
    max = array[k]

    for i in range(0, len(array)):
        if array[i] > max:
            max = array[i]
            k = i

    return k

def getMax(array):
    k = 0
    max = array[k]

    for i in range(0, len(array)):
        if array[i] > max:
            max = array[i]
            k = i

    return max

training = [
    # [[5, 10], 20],
    # [[6, 12], 24],
    # [[9, 18], 36]
]

for i in range(0, 100):
    training.append([])
    var = np.random.randint(20)

    for j in range(0, 2):
        if (j%2) == 0:
            training[i].append([sigmoid(var), sigmoid(2*var)])
        else:
            training[i].append(sigmoid(4*var))

values = []
answer = []

for i in range(0, len(training)):
    for j in range(0, len(training[i])):
        if (j % 2) == 0:
            values.append(training[i][j])
        else:
            answer.append(training[i][j])

class Neural_Network():

    def __init__(self, layers):
        self.layers = layers
        self.wb = [] #weights and biases
        self.best = [] #best weights and biases

        # for i in range(0, self.layers.__len__()-1):
        #     self.wb.append([])
        #     for j in range(0, self.layers[i+1]):
        #         self.wb[i].append([])
        #         for k in range(0, self.layers[i]+1):
        #             self.wb[i][j].append(random.random())

        self.wb = [[[169.9187940715953, -49.76116412192303, 33.53736055705731, 295.1473552455269, -200.6279246004753, 64.7498230042388, 0.034607719445303164], [-4.910139460815705, -97.47998735419782, -38.85434208125214, 284.18005877584966, 116.16094978081475, -115.65539640651276, 0.8438650698113874], [24.295491544389172, 143.44944881925792, -69.71347446691416, -186.002755927534, 6.709436280895936, -14.783962264491894, 0.2254378182087965], [307.62265829817704, 280.65222396522296, 188.76128632710456, 32.1521136155177, -215.2182784007199, -2.3004157257050917, 0.07457733770530017]]]

        self.best = self.wb

    def func(self, input):
        neurons = []

        for i in range(0, len(self.layers)):
            neurons.append([])
            for j in range (0, self.layers[i]):
                neurons[i].append(0)

        neurons[0] = input

        for i in range(0, len(self.layers)-1): #previous layer
            for j in range(0, self.layers[i+1]): #current neuron
                tempVar = 0
                for k in range(0, self.layers[i]): #previous layer's neurons
                    tempVar += neurons[i][k] * self.wb[i][j][k]
                    tempVar += self.wb[i][j][k+1]
                neurons[i+1][j] = sigmoid(tempVar)
        return neurons[len(self.layers)-1]

    def getAnswer(self, input):
        return getMaxIndex(self.func(input))

    def getCost(self, val, answer):
        return m_sum(m_pow(m_sub(self.func(val), [answer]), 2))

    def bestWB(self):
        self.best = copy.deepcopy(self.wb)

    def neat(self, alpha):
        for i in range(0, len(self.layers) - 1):  # previous layer
            for j in range(0, self.layers[i + 1]):  # current neuron
                for k in range(0, self.layers[i]):  # previous layer's neurons
                    self.wb[i][j][k] = self.best[i][j][k] + alpha * (random.random()-0.5)