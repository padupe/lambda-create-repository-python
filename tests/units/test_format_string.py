from ast import For
import pytest
from helpers import format_string as Format

STRING_UPPER_UNDERLINE="TEST_FUNCTION"
STRING_UPPER_BLANK_SPACE="TEST FUNCTION"

def test_function_format_string_with_underline_success():
    fn = Format.format_string(STRING_UPPER_UNDERLINE)
    assert fn == "test_function"
    
def test_function_format_string_with_blank_space_success():
    fn = Format.format_string(STRING_UPPER_BLANK_SPACE)
    assert fn == "test-function"
    
def test_function_format_string_with_int_value_failure():
    with pytest.raises(AttributeError):
        Format.format_string(1234)
        