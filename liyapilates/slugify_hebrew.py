# -*- coding: utf-8 -*-
import re
import unicodedata

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')

hebrew = u'אבגדהוזחטיכךלמםנןסעפףצקרשת'
english = ['a', 'b', 'g', 'd', 'h', 'v', 'z', 'gh', 't', 'i', 'c', 'ch', 'l', 'm', 'm', 'n', 'n', 's', 'a', 'p', 'f',
           'tz', 'ts', 'k', 'r', 'sh', 'th']
result = ''
name = u'מילה, woORd and גם += עם סימ₪*נחם'

for i in name:
    indx = hebrew.find(i, 0)
    if indx == -1:
        result += i
    else:
        result += english[indx]

if not isinstance(result, unicode):
    result = unicode(result)
result = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore')
result = unicode(_slugify_strip_re.sub('', result).strip().lower())

print
_slugify_hyphenate_re.sub('-', result)
