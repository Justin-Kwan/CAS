import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuthentication/server/src')
from InputSanitizer import InputSanitizer

inputSanitizer = InputSanitizer()

def test_sanitizeUsername():
    assert inputSanitizer.sanitizeUsername("string") == "string"
    assert inputSanitizer.sanitizeUsername("fake$username)") == "fakeusername"
    assert inputSanitizer.sanitizeUsername(")(*&^)") == ""
    assert inputSanitizer.sanitizeUsername(")(*&^)textTest*&^%moretestis*fun';:") == "textTestmoretestisfun"
