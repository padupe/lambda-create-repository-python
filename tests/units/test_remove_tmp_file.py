import pytest
import os
from helpers import remove_tmp_file as RemoveFile

file = open("myfile.txt", "x")

def test_function_remove_tmp_file_success():
    with pytest.raises(FileNotFoundError):
        tmp = RemoveFile.remove_tmp_file(file)
        assert tmp == os.remove(file.name)
        
def test_function_remove_tmp_file_failure():
    with pytest.raises(ValueError, match=r".deleting file .*"):
        RemoveFile.remove_tmp_file(file)
        raise ValueError(f"Error deleting file {file.name}.") 

os.remove(file.name)