import re

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
match = zhPattern.search('f2ewvwvdsacww你fedsvfejkl.ulk.,hmsvsvswf')

if match:
    print(1)
else:
    print(2)
