import re


class RegexHelper:
    pat_Text=r'[a-zA-Z ]+'
    pat_Number=r'[0-9]+'
    pat_Uppercase=r'[A-Z]+'
    pat_lowercase=r'[a-z]+'
    pat_specialChar=r'[$&+,:;=?@#|\'<>.^*_~`()%!/’‘’-]'
    pat_allAscii=r'[\x00-\xFF\'’‘’]+'
    pat_email=r'[A-Za-z0-9]+[\._]?[A-Za-z0-9]*@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}'
    pat_boolean=r'(yes|no|true|false)'
    pat_ipaddress=r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
    pat_url=r'[a-zA-Z]{4,6}://.+/?'
    pat_textArray=r'[a-zA-Z0-9 @\._]+[,;:|]'
    pat_float=r'[0-9]+\.[0-9]+'
    pat_datetime=r'(([0-9]{1,2}(\\|-|\/)[0-9]{1,2}\3[0-9]{4})|([0-9]{4}(\\|-|\/)[0-9]{1,2}\5[0-9]{1,2})) [0-9]{1,2}:[0-9]{1,2}(:[0-9]{1,2})?'
    pat_date=r'(([0-9]{1,2}(\\|-|\/)[0-9]{1,2}\3[0-9]{4})|([0-9]{4}(\\|-|\/)[0-9]{1,2}\5[0-9]{1,2}))'
    
    def get_textPattern(self):
        return self.pat_Text

    def get_numberPattern(self):
        return self.pat_Number

    def get_uppercasePattern(self):
        return self.pat_Uppercase
    
    def get_emailPattern(self):
        return self.pat_email

    def get_booleanPattern(self):
        return self.pat_boolean

    def get_ipPattern(self):
        return self.pat_ipaddress

    def get_urlPattern(self):
        return self.pat_url

    def get_textArrayPattern(self):
        return self.pat_textArray

    def get_floatPattern(self):
        return self.pat_float

    def get_datetimePattern(self):
        return self.pat_datetime

    def get_datePattern(self):
        return self.pat_date

    def get_specialCharPattern(self):
        return self.pat_specialChar

    def onlyText(self,value):
        if value is None:
            return False
        pat=self.pat_Text
        return True if re.fullmatch(pat,value) else False

    def onlyNumber(self,value):
        if value is None:
            return False
        pat=self.pat_Number
        return True if re.fullmatch(pat,value) else False

    def onlyupperCase(self,value):
        if value is None:
            return False
        pat=self.pat_Uppercase
        return True if re.fullmatch(pat,value) else False

    def hasUppercase(self,value):
        if value is None:
            return False
        pat=self.pat_Uppercase
        return True if re.search(pat,value) else False

    def hasSpecialChar(self,value):
        if value is None:
            return False
        pat=self.pat_specialChar
        return True if re.search(pat,value) else False

    def isEmail(self,value):
        if value is None:
            return False
        pat=self.pat_email
        return True if re.fullmatch(pat,value) else False

    def hasLowercase(self,value):
        if value is None:
            return False
        pat=self.pat_lowercase
        return True if re.search(pat,value) else False
    
    def hasWhiteSpace(self,value):
        if value is None:
            return False
        pat=r'[ ]'
        return True if re.search(pat,value) else False

    def hasNumber(self,value):
        if value is None:
            return False
        pat=self.pat_Number
        return True if re.search(pat,value) else False
    
    def determineTextRegexLevel(self,value):
        regex_wild_card=''
        value=str(value)
        
        if self.hasSpecialChar(value):
            pat=self.pat_allAscii
            all_special=re.findall(pat,value)
            if len(all_special)<=2:
                if len(value)<40:
                    regex_wild_card+='\\'.join(set(all_special))
                else:
                    return '.+'
            else:
                return '.+'

        if self.hasLowercase(value):
            regex_wild_card+='a-z '

        if self.hasUppercase(value):
            regex_wild_card+='A-Z'

        if self.hasNumber(value):
            regex_wild_card+='0-9'

        return '['+regex_wild_card+']+'
        
