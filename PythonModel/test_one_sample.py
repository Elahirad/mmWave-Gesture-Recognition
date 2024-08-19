from CNN import CNNModel
from keras import models
import numpy as np

# Example usage
if __name__ == '__main__':
    model = models.load_model('model.keras')

    t = np.load('one_sample_to_test.npz')['prm_matrix']
    t = np.expand_dims(t, axis=(-1, 0))

    print(model.predict(t))
