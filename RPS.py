# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from sklearn import tree
import random

translate = {
    'R': {'translate': 0, 'choose': 'P'},
    'P': {'translate': 1, 'choose': 'S'},
    'S': {'translate': 2, 'choose': 'R'},
    0: {'translate': 'R'},
    1: {'translate': 'P'},
    2: {'translate': 'S'},
}

class Predictor:
    def __init__(self):
        self.clf = tree.DecisionTreeClassifier(max_depth=5, random_state=42)

    def train(self, X, y):
        self.clf.fit(X, y)

    def predict(self, current):
        return self.clf.predict([current])[0]

class DataCleaner:
    @staticmethod
    def numberize(string_arr):
        numberArray = [translate[x]['translate'] for x in string_arr]
        return numberArray
    @staticmethod
    def prepareData(numberArray):
        X = []
        y = []
        i = 0
        while(i + 2 < len(numberArray)):
            X.append([numberArray[i], numberArray[i+1]])
            y.append(numberArray[i+2])
            i+=1
        return (X, y)
    @staticmethod
    def prepareData(opponent_history, my_history):
        X = []
        y = []
        i = 0
        while(i + 2 < len(opponent_history)):
            X.append([ 
                opponent_history[i], opponent_history[i+1], 
                my_history[i], my_history[i+1]
                ])
            y.append(opponent_history[i+2])
            i+=1

        return (X, y)

predictor = Predictor()
dataCleaner = DataCleaner()
def player(prev_play, opponent_history=[], my_history=[]):
    if prev_play != '':
        opponent_history.append(prev_play)

    if len(opponent_history) > 999:
        opponent_history.clear()
        my_history.clear()

    if len(opponent_history) < 20:
        randomChoice = random.choice('RPS')
        my_history.append(randomChoice)
        return randomChoice

    int_opponent_history = dataCleaner.numberize(opponent_history)
    int_my_history = dataCleaner.numberize(my_history)

    if len(opponent_history) % 10 == 0 and len(opponent_history) > 19:
        X, y = dataCleaner.prepareData(int_opponent_history, int_my_history)
        predictor.train(X, y)

    last_moves = int_opponent_history[-2:] + int_my_history[-2:]
    pred = predictor.predict(last_moves)
    translatedPred = translate[pred]['translate']
    my_history.append(translatedPred)
    return translate[translatedPred]['choose']
