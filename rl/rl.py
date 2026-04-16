class UserPreferenceRL:

    def __init__(self):
        self.weights = {
            "price": 0.5,
            "distance": 0.3,
            "bedrooms": 0.2,
        }
        self.lr = 0.01

    def score(self, row):
        return (
            -self.weights["price"] * row["predicted_price"]
            - self.weights["distance"] * row["distance_to_station"]
            + self.weights["bedrooms"] * row["bedrooms"]
        )

    def update(self, row, feedback):
       
        direction = 1 if feedback == "like" else -1

        self.weights["price"] += direction * self.lr * (-row["predicted_price"])
        self.weights["distance"] += direction * self.lr * (-row["distance_to_station"])
        self.weights["bedrooms"] += direction * self.lr * row["bedrooms"]
