import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20, 12


def prepare_plot_data(df, lookback, predicted_train, predicted_test, max_ahead=False):
    if max_ahead:
        offset = lookback * 2
        index = -1
    else:
        offset = lookback
        index = 0

    predicted_train_plot = []
    for i in range(0, predicted_train.shape[0]):
        predicted_train_plot = np.append(
            predicted_train_plot, predicted_train[i, index])

    predicted_test_plot = []
    for i in range(0, predicted_test.shape[0]):
        predicted_test_plot = np.append(
            predicted_test_plot, predicted_test[i, index])

    measured = df[offset:]
    plot_X_train = df.index[offset:len(predicted_train_plot) + offset]
    plot_X_test = df.index[offset + len(predicted_train_plot):offset + len(
        predicted_train_plot) + len(predicted_test_plot)]
    return measured, plot_X_train, predicted_train_plot, plot_X_test, predicted_test_plot


def visualize_predictions(df, lookback, predicted_train, predicted_test, show_measured=True, max_ahead=False, train_color="salmon", test_color="red", label="predicted"):
    measured, plot_X_train, plot_y_train, plot_X_test, plot_y_test = prepare_plot_data(
        df, lookback, predicted_train, predicted_test, max_ahead)
    plt.subplot()
    if show_measured:
        plt.plot(measured.index, measured.humidity, color="gray")
    plt.plot(plot_X_train, plot_y_train,
             color=train_color, label=label + " train")
    plt.plot(plot_X_test, plot_y_test, color=test_color, label=label + " test")
    plt.legend()
