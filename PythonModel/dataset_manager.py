import os
import numpy as np

# Function to load the dataset
def load_dataset(root_dir='.'):
    X_data = []
    y_data = []
    all_entries = os.listdir(root_dir)
    classes = [entry for entry in all_entries if os.path.isdir(os.path.join(root_dir, entry))]
    
    for label, class_dir in enumerate(classes):
        print(f"{class_dir} -> {label}")
        class_path = os.path.join(root_dir, class_dir)
        class_data = []
        for file in os.listdir(class_path):
            if file.endswith('.npz'):
                data = np.load(os.path.join(class_path, file))['prm_matrix']
                class_data.append(data)
        
        # Convert class_data to a numpy array and shuffle it
        class_data = np.array(class_data)
        np.random.shuffle(class_data)
        
        # Pick the first 3000 samples (or fewer if not enough samples)
        selected_data = class_data[:3000]
        
        # Append the selected data and labels
        X_data.extend(selected_data)
        y_data.extend([label] * len(selected_data))

    X = np.array(X_data)
    y = np.array(y_data)
    # Randomize (shuffle) the dataset
    indices = np.random.permutation(X.shape[0])
    X = X[indices]
    y = y[indices]
    return X, y

def load_and_save_dataset(root_dir='.', output_path='Dataset.npz'):
    X, y = load_dataset(root_dir)
    np.savez_compressed(output_path, X=X, y=y)

def load_saved_dataset(path):
    f = np.load(path)
    X, y = f['X'], f['y']
    return X, y

if __name__ == '__main__':
    load_and_save_dataset('dataset')
    

