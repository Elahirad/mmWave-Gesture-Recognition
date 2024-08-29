from CNN import CNNModel
from keras import models
import numpy as np
import os


def test_samples_from_folder(dir_name, model_file_name):
    model = models.load_model(
        os.path.join(os.getcwd(), model_file_name),
        custom_objects={"CNNModel": CNNModel},
    )
    c = {}
    total_count = 0
    for dir in os.listdir(os.path.join(os.getcwd(), dir_name)):
        file_path = os.path.join(os.getcwd(), dir_name, dir)
        if os.path.isfile(file_path):
            total_count += 1
            t = np.load(file_path)["prm_matrix"]
            t = np.expand_dims(t, axis=(-1, 0))
            pr = model.predict(t)[0]
            idx = next((i for i, v in enumerate(pr) if v == max(pr)), -1)
            if idx not in c:
                c[idx] = 1
            else:
                c[idx] += 1

    for key, value in c.items():
        print("Results:")
        print("Class {0} -> {1:.2f}%".format(key, value / total_count * 100))


if __name__ == "__main__":
    test_samples_from_folder("test_samples", "model.keras")
