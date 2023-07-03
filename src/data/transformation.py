from sklearn.preprocessing import MinMaxScaler

class TransformTarget():
    def __init__(self, feature_range=(0,1)):
        self.feature_range = feature_range
    def fit(self, X=None, y=None):
        self.target_scaler = MinMaxScaler(self.feature_range)
        self.target_scaler.fit(y)
    def transform(self, X=None, y=None):
        y = self.target_scaler.transform(y)
        return y