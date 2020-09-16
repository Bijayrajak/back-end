from portalservices.regexengine import RegexHelper
import re

def onlyText(value):
    if value is None:
        return False
    pat=RegexHelper.pat_Text
    return True if re.fullmatch(pat,value) else False

def onlyNumber(value):
    if value is None:
        return False
    pat=RegexHelper.pat_Number
    return True if re.fullmatch(pat,value) else False

def onlyupperCase(value):
    if value is None:
        return False
    pat=RegexHelper.pat_Uppercase
    return True if re.fullmatch(pat,value) else False

def hasUppercase(value):
    if value is None:
        return False
    pat=RegexHelper.pat_Uppercase
    return True if re.search(pat,value) else False

def hasNumber(value):
    if value is None:
        return False
    pat=RegexHelper.pat_Number
    return True if re.search(pat,value) else False

def hasSpecialChar(value):
    if value is None:
        return False
    pat=RegexHelper.pat_specialChar
    return True if re.search(pat,value) else False

def isEmail(value):
    if value is None:
        return False
    pat=RegexHelper.pat_email
    return True if re.fullmatch(pat,value) else False

def hasLowercase(value):
    if value is None:
        return False
    pat=RegexHelper.pat_lowercase
    return True if re.search(pat,value) else False

def hasDotUnderscoreOnly(value):
    if value is None:
        return False
    
    pat=RegexHelper.pat_specialChar
    all_special=re.findall(pat,value)
    if set(all_special)-set(['_','.']):
        return False
    else:
        return True




