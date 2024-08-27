from CNN import CNNModel
from keras import models
import numpy as np

# Example usage
if __name__ == "__main__":
    model = models.load_model("model.keras", custom_objects={"CNNModel": CNNModel})

    t = np.load("sample_219.npz")["prm_matrix"]
    # t = np.array(list(map(lambda x: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], range(20))))
    print(t)
    t = np.expand_dims(t, axis=(-1, 0))

    print(model.predict(t))
