import os
import shutil

def map_users_to_files(directory):
    user_file_map = []

    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            user = {}
            user['dirs'] = {}
            c = 1e10
            for dir in os.listdir(os.path.join(directory, item)):
                if dir not in ['other', 'run']:
                    os.makedirs(os.path.join('Out', dir), exist_ok=True)
                    files = os.listdir(os.path.join(directory, item, dir))
                    if len(files) < c:
                        c = len(files)
                    user['dirs'][dir] = list(map(lambda f: os.path.join(directory, item, dir, f), files))
            user['min_samples'] = c
            user_file_map.append(user)
    
    return user_file_map


def pick_main_motions(directory, samples_from_each_user, output_folder_name):
    k = {}
    os.makedirs(output_folder_name, exist_ok=True)
    for user in map_users_to_files(directory):
        samples_to_pick = user['min_samples'] if user['min_samples'] < samples_from_each_user else samples_from_each_user
        for dir, files in user['dirs'].items():
            for i in range(samples_to_pick):
                if dir not in k.keys():
                    k[dir] = 1
                else:
                    k[dir] += 1
                source = files[i]
                dest = os.path.join(os.getcwd(), 'Out', dir, f"sample_{k[dir]}.npz")
                shutil.copy2(source, dest)
                print(f"Copied {source} -> {dest}")
            
     
def pick_unex_motions(directory, output_folder_name):
    k = 1 
    os.makedirs(output_folder_name, exist_ok=True)
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            for dir in os.listdir(os.path.join(directory, item)):
                if dir in ['other', 'run']:
                    os.makedirs(os.path.join('Out', 'unex'), exist_ok=True)
                    files = list(map(lambda f: os.path.join(directory, item, dir, f), os.listdir(os.path.join(directory, item, dir))))
                    for file in files:
                        source = file
                        dest = os.path.join(os.getcwd(), 'Out', 'unex', f"sample_{k}.npz")
                        shutil.copy2(source, dest)
                        k += 1
                        print(f"Copied {source} -> {dest}")


if __name__ == "__main__":
    folder = 'Transform_Output'

    directory = os.path.join(os.getcwd(), folder)

    pick_main_motions(directory, 50, 'Out')

    pick_unex_motions(directory, 'Out')