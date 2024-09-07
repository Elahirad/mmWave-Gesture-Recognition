import os
import numpy as np


def load_dataset(samples_from_each_class, root_dir=".", label_offset=0):
    X_data = []
    y_data = []
    all_entries = os.listdir(root_dir)
    classes = [
        entry for entry in all_entries if os.path.isdir(os.path.join(root_dir, entry))
    ]

    for label, class_dir in enumerate(classes):
        label_to_reg = label + label_offset
        print(f"{class_dir} -> {label_to_reg}")
        class_path = os.path.join(root_dir, class_dir)
        class_data = []
        for file in os.listdir(class_path):
            if file.endswith(".npz"):
                data = np.load(os.path.join(class_path, file))["prm_matrix"]
                class_data.append(data)

        class_data = np.array(class_data)
        np.random.shuffle(class_data)

        selected_data = class_data[:samples_from_each_class]

        X_data.extend(selected_data)
        y_data.extend(
            [
                [1 if i == label_to_reg else 0 for i in range(5)]
                for j in range(len(selected_data))
            ]
        )

    X = np.array(X_data)
    y = np.array(y_data)

    return X, y


def shuffle_dataset(X, y):
    indices = np.random.permutation(X.shape[0])
    X = X[indices]
    y = y[indices]
    return X, y


def save_dataset(X, y, output_path):
    np.savez_compressed(output_path, X=X, y=y)


def load_saved_dataset(path):
    f = np.load(path)
    X, y = f["X"], f["y"]
    return X, y


def augment_angle(X, y):
    X = np.copy(X)
    y = np.copy(y)
    angle_offsets = np.random.normal(0, 2, (X.shape[0], 1))
    for i in range(X.shape[0]):
        X[i, :, 9] += angle_offsets[i]

    return X, y


def augment_range(X, y):
    X = np.copy(X)
    y = np.copy(y)
    range_offsets = np.random.normal(0, 2, (X.shape[0], 1))
    for i in range(X.shape[0]):
        X[i, :, 1] += range_offsets[i]
        X[i, :, 4] += range_offsets[i]
        X[i, :, 7] += range_offsets[i]

    return X, y


def augment_velocity(X, y):
    X = np.copy(X)
    y = np.copy(y)
    velocity_factors = np.random.normal(1, 0.25, (X.shape[0], 1))
    for i in range(X.shape[0]):
        X[i, :, 2] *= velocity_factors[i]
        X[i, :, 5] *= velocity_factors[i]
        X[i, :, 8] *= velocity_factors[i]

    return X, y


def augment_time(X, y):
    X = np.copy(X)
    y = np.copy(y)
    offsets = np.random.randint(-10, 10, (X.shape[0], 1))
    for i in range(X.shape[0]):
        X[i] = np.roll(X[i], offsets[i], axis=0)

    return X, y


def augment_noise(X, y):
    X = np.copy(X)
    y = np.copy(y)
    noise = np.random.normal(0, 0.05, X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            cp = np.floor(X[i, j, 3] / 2)
            cf = np.floor(X[i, j, 6] / 2)
            noise[i, j, 0] = -(cp + cf)
            noise[i, j, 3] = -cp
            noise[i, j, 6] = -cf

    X += noise

    return X, y


if __name__ == "__main__":

    X, y = load_dataset(2900, "dataset")

    X_ang, y_ang = augment_angle(X, y)
    X_noise, y_noise = augment_noise(X, y)
    X_time, y_time = augment_time(X, y)
    X_range, y_range = augment_range(X, y)
    X_velocity, y_velocity = augment_velocity(X, y)

    X = np.append(X, X_ang, axis=0)
    y = np.append(y, y_ang, axis=0)

    X = np.append(X, X_noise, axis=0)
    y = np.append(y, y_noise, axis=0)

    X = np.append(X, X_time, axis=0)
    y = np.append(y, y_time, axis=0)

    X = np.append(X, X_range, axis=0)
    y = np.append(y, y_range, axis=0)

    X = np.append(X, X_velocity, axis=0)
    y = np.append(y, y_velocity, axis=0)

    X_unex, y_unex = load_dataset(2900, "unex_dataset", 4)

    X = np.append(X, X_unex, axis=0)
    y = np.append(y, y_unex, axis=0)

    X, y = shuffle_dataset(X, y)

    save_dataset(X, y, "Dataset.npz")

    X, y = load_dataset(100, "valset")

    X, y = shuffle_dataset(X, y)

    save_dataset(X, y, "Valset.npz")

    X, y = load_dataset(100, "testset")

    save_dataset(X, y, "Testset.npz")
