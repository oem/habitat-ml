import numpy as np
import matplotlib.pylab as plt


def get_1h(t): return t[0]


def get_24h(t): return t[-1]


def plot_histograms(diff_train, diff_test):
    train_1h = np.array([get_1h(x) for x in diff_train])
    train_24h = np.array([get_24h(x) for x in diff_train])
    test_1h = np.array([get_1h(x) for x in diff_test])
    test_24h = np.array([get_24h(x) for x in diff_test])

    plt.hist(train_1h, color="blue",
             label="training set: predicted 1h difference")
    plt.hist(train_24h, color="violet", alpha=0.5,
             label="training set: predicted 24h difference")
    plt.legend()

    plt.figure()
    plt.hist(test_1h, color="orange",
             label="test set: predicted 1h difference")
    plt.hist(test_24h, color="yellow", alpha=0.5,
             label="test set: predicted 24h difference")
    plt.legend()

    plt.show()
