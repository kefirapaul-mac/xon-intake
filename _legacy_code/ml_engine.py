import numpy as np
from sklearn.linear_model import LogisticRegression


class RetentionModel:

    def __init__(self):
        self.model = LogisticRegression()
        self._train()

    def _train(self):
        # Synthetic dataset
        X = np.array([
            [6, 6, 6],
            [8, 7, 9],
            [3, 4, 2],
            [9, 8, 9],
            [5, 5, 5],
            [2, 3, 2],
            [7, 7, 8]
        ])

        y = np.array([1, 1, 0, 1, 1, 0, 1])

        self.model.fit(X, y)

    def predict(self, features):
        prediction = self.model.predict([features])[0]
        probability = self.model.predict_proba([features])[0][1]
        return round(probability * 36, 1)  # months retention projection