import numpy as np
import tensorflow as tf
from keras import layers, optimizers, callbacks
from dataset_manager import load_saved_dataset


class CNNModel(tf.keras.Sequential):
    def __init__(self, *args, **kwargs):
        super(CNNModel, self).__init__(*args, **kwargs)

    def build_model(self, input_shape, num_classes):
        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(7, 7),
                strides=(2, 2),
                padding="same",
                input_shape=input_shape,
            )
        )

        self.add(layers.BatchNormalization())

        self.add(layers.Dropout(0.3))

        self.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same"))

        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
            )
        )

        self.add(layers.BatchNormalization())
        self.add(layers.ReLU())

        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
            )
        )

        self.add(layers.BatchNormalization())

        self.add(layers.Dropout(0.3))

        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
            )
        )

        self.add(layers.BatchNormalization())

        self.add(layers.ReLU())

        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
            )
        )

        self.add(layers.BatchNormalization())

        self.add(layers.Dropout(0.3))

        self.add(layers.Flatten())

        self.add(
            layers.Dense(
                256,
                activation=None,
                kernel_regularizer=tf.keras.regularizers.l2(0.05),
            )
        )

        self.add(layers.BatchNormalization())

        self.add(layers.Dropout(0.3))

        self.add(
            layers.Dense(
                num_classes,
                activation="softmax",
                kernel_regularizer=tf.keras.regularizers.l2(0.05),
            )
        )

    def compile_model(self, learning_rate):
        optimizer = optimizers.Adam(learning_rate=learning_rate)
        self.compile(
            optimizer=optimizer,
            loss="categorical_crossentropy",
            metrics=["categorical_accuracy"],
        )

    def load_and_prepare_train_data(self, dataset_name):
        X, y = load_saved_dataset(dataset_name)

        X = np.expand_dims(X, axis=-1)

        self.X_train = X
        self.y_train = y

    def load_and_prepare_test_data(self, dataset_name):
        X, y = load_saved_dataset(dataset_name)

        X = np.expand_dims(X, axis=-1)

        self.X_test = X
        self.y_test = y

    def load_and_prepare_val_data(self, dataset_name):
        X, y = load_saved_dataset(dataset_name)

        X = np.expand_dims(X, axis=-1)

        self.X_val = X
        self.y_val = y

    def train(self, epochs=60, batch_size=32):
        def scheduler(epoch, lr):
            if epoch != 0 and epoch % 20 == 0:
                return lr * 0.1
            return lr

        lr_callback = callbacks.LearningRateScheduler(scheduler)

        early_stopping = callbacks.EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True
        )
        self.fit(
            self.X_train,
            self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.X_val, self.y_val),
            callbacks=[lr_callback, early_stopping],
        )

    def evaluate_model(self):
        test_loss, test_acc = self.evaluate(self.X_test, self.y_test, verbose=2)
        print(f"Test Loss: {test_loss}\nTest accuracy: {test_acc}")
        return test_acc

    def save_model(self, model_path="model.keras"):
        self.save(model_path)


if __name__ == "__main__":

    input_shape = (20, 10, 1)

    cnn_model = CNNModel()
    cnn_model.build_model(input_shape, 5)
    cnn_model.compile_model(0.0001)
    cnn_model.load_and_prepare_train_data("Dataset.npz")
    cnn_model.load_and_prepare_val_data("Valset.npz")
    cnn_model.load_and_prepare_test_data("Testset.npz")
    cnn_model.summary()
    cnn_model.train(epochs=40, batch_size=128)
    cnn_model.evaluate_model()
    cnn_model.save_model("model.keras")
    tf.saved_model.save(cnn_model, "model")
