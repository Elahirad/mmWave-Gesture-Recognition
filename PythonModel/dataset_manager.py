import os
import numpy as np
from random import randint
from math import floor


# Function to load the dataset
def load_dataset(samples_from_each_class, root_dir="."):
    X_data = []
    y_data = []
    all_entries = os.listdir(root_dir)
    classes = [
        entry for entry in all_entries if os.path.isdir(os.path.join(root_dir, entry))
    ]

    for label, class_dir in enumerate(classes):
        print(f"{class_dir} -> {label}")
        class_path = os.path.join(root_dir, class_dir)
        class_data = []
        for file in os.listdir(class_path):
            if file.endswith(".npz"):
                data = np.load(os.path.join(class_path, file))["prm_matrix"]
                class_data.append(data)

        # Convert class_data to a numpy array and shuffle it
        class_data = np.array(class_data)
        np.random.shuffle(class_data)

        # Pick the first 3000 samples (or fewer if not enough samples)
        selected_data = class_data[:samples_from_each_class]

        # Append the selected data and labels
        X_data.extend(selected_data)
        y_data.extend(
            [
                [1 if i == label else 0 for i in range(5)]
                for j in range(len(selected_data))
            ]
        )

    X = np.array(X_data)
    y = np.array(y_data)

    return X, y


def augment_dataset(X_orig, y_orig):

    X = np.copy(X_orig)
    y = np.copy(y_orig)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            ncp = randint(0, floor(X[i, j, 3] / 2))
            ncf = randint(0, floor(X[i, j, 6] / 2))
            nec = ncp + ncf
            X[i, j, 3] -= ncp
            X[i, j, 6] -= ncf
            X[i, j, 0] -= nec

    random_matrix = 1 * (np.random.rand(X.shape[0], X.shape[1], 7) - 0.5)

    diff = np.zeros((X.shape[0], X.shape[1], 10))

    diff[:, :, 1:3] = random_matrix[:, :, 0:2]

    diff[:, :, 4:6] = random_matrix[:, :, 2:4]

    diff[:, :, 7:10] = random_matrix[:, :, 4:7]

    X = X + np.abs(np.sign(X)) * diff

    X = np.append(X_orig, X, axis=0)
    y = np.append(y_orig, y, axis=0)

    return X, y


def shuffle_dataset(X, y):
    indices = np.random.permutation(X.shape[0])
    X = X[indices]
    y = y[indices]
    return X, y


def load_and_save_dataset(
    samples_from_each_class, root_dir=".", output_path="Dataset.npz"
):
    X, y = load_dataset(samples_from_each_class, root_dir)
    np.savez_compressed(output_path, X=X, y=y)


def load_augment_save_dataset(
    samples_from_each_class, root_dir=".", output_path="AUG_Dataset.npz"
):
    X, y = load_dataset(samples_from_each_class, root_dir)
    X, y = augment_dataset(X, y)
    np.savez_compressed(output_path, X=X, y=y)


def load_augment_shuffle_dataset(
    samples_from_each_class, root_dir=".", output_path="AUG_Shuffled_Dataset.npz"
):
    X, y = load_dataset(samples_from_each_class, root_dir)
    X, y = augment_dataset(X, y)
    X, y = shuffle_dataset(X, y)
    np.savez_compressed(output_path, X=X, y=y)


def load_saved_dataset(path):
    f = np.load(path)
    X, y = f["X"], f["y"]
    return X, y


if __name__ == "__main__":
    samples_from_each_class = 3000
    load_augment_shuffle_dataset(samples_from_each_class, "dataset")
