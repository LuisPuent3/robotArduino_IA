from sklearn.tree import DecisionTreeRegressor
import numpy as np

def entrenar_modelo(X, y):
    model = DecisionTreeRegressor()
    model.fit(X, y)
    return model
