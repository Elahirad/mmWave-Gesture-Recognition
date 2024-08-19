from SEP_to_PRM import process_and_save_prm_matrices

import os

main_dir = 'long_SEP'


for dir in os.listdir(main_dir):
    path = os.path.join(main_dir, dir)
    if os.path.isdir(path):
        for file in os.listdir(path):
            gesture = file.split('_')[-1].split('.')[0]
            process_and_save_prm_matrices(os.path.join(os.getcwd(), path, file), os.path.join(os.getcwd(), 'Transform_Output', dir, gesture))
            
