import os

def remove_tmp_file(file):
    
    if os.path.exists(file.name):
        os.remove(file.name)
    else:
        return {
            "status": 500,
            "message": f'Error deleting file {file.name}.'
        }