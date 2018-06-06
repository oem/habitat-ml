from sklearn.model_selection import train_test_split


def prepare_test_train(dataset, lookback, test_size=0.2):
    X, y = [], []
    for i in range(lookback, len(dataset) - lookback):
        X.append(dataset[i-lookback:i])
        y.append(dataset[i:i+lookback])
    return train_test_split(X, y, test_size=test_size, shuffle=False)
