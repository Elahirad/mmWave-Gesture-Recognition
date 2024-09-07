from CNN import CNNModel
from keras import models
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
)
import matplotlib.pyplot as plt
import numpy as np
import os

from dataset_manager import load_saved_dataset


def analyze_dataset_results(X, y, model_name):
    model = models.load_model(
        os.path.join(os.getcwd(), model_name),
        custom_objects={"CNNModel": CNNModel},
    )

    X = np.expand_dims(X, axis=(-1))

    y_pred = model.predict(X)

    y_pred = y_pred.argmax(axis=1)

    y = y.argmax(axis=1)

    labels = ("Knock", "LSwipe", "Rotate", "RSwipe", "Unexpected")

    cm = confusion_matrix(y, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=labels,
    )

    print(
        f'Precision={precision_score(y, y_pred, average="weighted", zero_division=0.0) * 100}%'
    )
    print(
        f'Recall={recall_score(y, y_pred, average="weighted", zero_division=0.0) * 100}%'
    )
    print(
        f'F1 Score={f1_score(y, y_pred, average="weighted", zero_division=0.0) * 100}%'
    )

    disp.plot()

    plt.show()


if __name__ == "__main__":
    X, y = load_saved_dataset("Testset.npz")
    analyze_dataset_results(X, y, "model.keras")
