import os
import shutil
import zipfile

def create_zip_from_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def cleanup_tmp_files(zip_path: str, temp_dir: str):
    def cleanup():
        try:
            if os.path.exists(zip_path):
                os.remove(zip_path)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"清理临时文件时出错: {e}")
    
    return cleanup