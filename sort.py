import shutil
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def main(path):
    list_folders = []
    list_files = []
    filtered_list_files = []
    filtered_list_folders = []
    lists_unk_files = []
    remove_list = []
    path_images = create_dir(path, 'images')
    path_documents = create_dir(path, 'documents')
    path_audio = create_dir(path, 'audio')
    path_video = create_dir(path, 'video')
    path_archives = create_dir(path, 'archives')
    path_unknown_files = create_dir(path, 'Unknown_files')
    ignore_dir = [f'{path_images}', f'{path_documents}', f'{path_audio}',
                  f'{path_video}', f'{path_archives}', f'{path_unknown_files}']

    for root, dirs, files in os.walk(path):
        for folder in dirs:
            folders_path = os.path.join(root, folder)
            list_folders.append(folders_path)

        for file in files:
            files_path = os.path.join(root, file)
            list_files.append(files_path)

    for ignor_files in list_files:
        if not any(new_files in ignor_files for new_files in ignore_dir):
            filtered_list_files.append(ignor_files)

    for ignor_folders in list_folders:
        if not any(new_folders in ignor_folders for new_folders in ignore_dir):
            filtered_list_folders.append(ignor_folders)

    def move_files(files_form_list):
        name_of_files = os.path.basename(files_form_list)
        file_name = os.path.splitext(name_of_files)[0]
        file_suf = os.path.splitext(name_of_files)[1]
        if file_suf.upper() in lists_img:
            new_path = os.path.join(path_images, f'{file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_vid:
            new_path = os.path.join(path_video, f'{file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_doc:
            new_path = os.path.join(path_documents, f'{file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_mus:
            new_path = os.path.join(path_audio, f'{file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_arch:
            try:
                new_path = os.path.join(path_archives, f'{file_name}')
                shutil.unpack_archive(files_form_list, new_path)
                os.remove(files_form_list)
            except Exception:
                print(f"Can't unpack: {name_of_files}")
                os.remove(files_form_list)
        elif file_suf.upper() not in lists_suf:
            lists_unk_files.append(f'{name_of_files}')
            new_path = os.path.join(path_unknown_files, f'{name_of_files}')
            os.rename(files_form_list, new_path)

    def move_folders(folders_from_list):
        contents = os.listdir(folders_from_list)
        if not contents:
            remove_list.append(folders_from_list)
        for rem in remove_list:
            os.rmdir(rem)

    with ThreadPoolExecutor() as executor:
        executor.map(move_files, filtered_list_files)
        executor.map(move_folders, filtered_list_folders)

    new_filtered_list_folders = [item for item in filtered_list_folders if item not in remove_list]

    for folders_from_list in new_filtered_list_folders:
        name_of_fold = os.path.basename(folders_from_list)
        path_components = folders_from_list.split(os.sep)
        path_components[-1] = name_of_fold
        path_for_new_name = os.sep.join(path_components)
        os.rename(folders_from_list, path_for_new_name)

    if len(new_filtered_list_folders) >= 1:
        main(folder_path)
    else:
        print('Done!')


def create_dir(dir_path, name):
    path_for_dir_1 = os.path.join(dir_path, name)
    path_for_dir_1 = Path(path_for_dir_1)
    try:
        path_for_dir_1.mkdir()
        my_path = str(path_for_dir_1)
        return my_path
    except Exception:
        my_path = str(path_for_dir_1)
        return my_path


lists_img = ['.JPEG', '.PNG', '.JPG', '.SVG']
lists_vid = ['.AVI', '.MP4', '.MOV', '.MKV']
lists_doc = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
lists_mus = ['.MP3', '.OGG', '.WAV', '.AMR']
lists_arch = ['.ZIP', '.GZ', '.TAR']
lists_suf = lists_img + lists_vid + lists_doc + lists_mus + lists_arch

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    folder_path = sys.argv[1]
    main(folder_path)
