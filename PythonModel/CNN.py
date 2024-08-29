from typing import Callable
import numpy as np
import tensorflow as tf
from keras import layers, models, optimizers, callbacks
from sklearn.model_selection import train_test_split
from dataset_manager import load_saved_dataset


class CNNModel(tf.keras.Sequential):
    def __init__(self, *args, **kwargs):
        super(CNNModel, self).__init__(*args, **kwargs)

    def build_model(self, input_shape, num_classes):
        # Convolution Layer 1: 7x7 kernel, 2x2 stride, 'same' padding
        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(7, 7),
                strides=(2, 2),
                padding="same",
                input_shape=input_shape,
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )

        # Max Pooling Layer: 3x3 pool size, 2x2 stride
        self.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same"))

        # Convolution Layer 2: 3x3 kernel, 1 stride, 'same' padding
        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )

        # Rectified Linear Unit (ReLU) Activation
        self.add(layers.Activation("relu"))

        # Convolution Layer 3: 3x3 kernel, 1 stride, 'same' padding
        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )

        # Convolution Layer 4: 3x3 kernel, 1 stride, 'same' padding
        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )

        # Rectified Linear Unit (ReLU) Activation
        self.add(layers.Activation("relu"))

        # Convolution Layer 5: 3x3 kernel, 1 stride, 'same' padding
        self.add(
            layers.Conv2D(
                filters=128,
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )

        # Flatten the output to feed into fully connected layers
        self.add(layers.Flatten())

        self.add(
            layers.Dense(
                256,
                activation=None,
                kernel_regularizer=tf.keras.regularizers.l2(0.05),
            )
        )

        self.add(
            layers.Dense(
                num_classes,
                activation=None,
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )

        self.add(layers.Softmax())

    def compile_model(self, learning_rate):
        optimizer = optimizers.Adam(learning_rate=learning_rate)
        self.compile(
            optimizer=optimizer,
            loss="categorical_crossentropy",
            metrics=["categorical_accuracy"],
        )

    def load_and_prepare_data(self, dataset_loader: Callable, test_size=0.05):
        # Load the dataset
        X, y = dataset_loader()

        # Reshape the dataset to include the channel dimension
        X = np.expand_dims(X, axis=-1)

        # Split the dataset into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size
        )
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            self.X_train, self.y_train, test_size=0.05
        )

    def train(self, epochs=60, batch_size=32):
        # Define a learning rate scheduler
        def scheduler(epoch, lr):
            if epoch != 0 and epoch % 20 == 0:
                return lr * 0.1
            return lr

        lr_callback = callbacks.LearningRateScheduler(scheduler)

        # Define early stopping callback
        # early_stopping = callbacks.EarlyStopping(
        #     monitor="val_loss", patience=10, restore_best_weights=True
        # )
        # callbacks_arr = [lr_callback, early_stopping]
        callbacks_arr = [lr_callback]
        # Train the model with the learning rate scheduler
        self.fit(
            self.X_train,
            self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.X_val, self.y_val),
            callbacks=callbacks_arr,
        )

    def evaluate_model(self):
        # Evaluate the model
        test_loss, test_acc = self.evaluate(self.X_test, self.y_test, verbose=2)
        print(f"Test Loss: {test_loss}\nTest accuracy: {test_acc}")
        return test_acc

    def save_model(self, model_path="model.keras"):
        # Save the model
        self.save(model_path)


# Example usage
if __name__ == "__main__":

    def load_dataset():
        return load_saved_dataset("AUG_Dataset.npz")

    input_shape = (20, 10, 1)  # Adjusted input shape

    cnn_model = CNNModel()
    cnn_model.build_model(input_shape, 5)
    cnn_model.compile_model(0.0001)
    cnn_model.load_and_prepare_data(load_dataset)
    cnn_model.summary()
    cnn_model.train(epochs=40, batch_size=16)
    cnn_model.evaluate_model()
    cnn_model.save_model("model.keras")
    tf.saved_model.save(cnn_model, "model")
