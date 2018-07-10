#!/usr/bin/python3
# -*- coding: utf-8 -*-

ch1 = 'A'
ch2 = '中'

print("en u8:\t", ch1.encode('utf-8'))
print("en u8:\t", ch2.encode('utf-8'))
# en u8:   b'A'
# en u8:   b'\xe4\xb8\xad'

print("en u8, de uni:\t", ch1.encode('utf-8').decode('unicode_escape'))
print("en u8, de uni:\t", ch2.encode('utf-8').decode('unicode_escape'))
# en u8, de uni:   A
# en u8, de uni:   ä¸­

print("en u8, de uni, en u8:\t", ch1.encode('utf-8').decode('unicode_escape').encode('utf-8'))
print("en u8, de uni, en u8:\t", ch2.encode('utf-8').decode('unicode_escape').encode('utf-8'))
# en u8, de uni, en u8:    b'A'
# en u8, de uni, en u8:    b'\xc3\xa4\xc2\xb8\xc2\xad'

print("en gb:\t", ch1.encode('gb2312'))
print("en gb:\t", ch2.encode('gb2312'))
# en gb:   b'A'
# en gb:   b'\xd6\xd0'

print("en gb:\t, de uni", ch1.encode('gb2312').decode('unicode_escape'))
print("en gb:\t, de uni", ch2.encode('gb2312').decode('unicode_escape'))
# en gb:  , de uni A
# en gb:  , de uni ÖÐ

print("en gb:\t", ch1.encode('unicode_escape'))
print("en gb:\t", ch2.encode('unicode_escape'))
# en gb:   b'A'
# en gb:   b'\\u4e2d'

print(ch2.encode('unicode_escape'))     # b'\\u4e2d'
print(ch2.encode('unicode_escape').decode('utf-8'))     # '\u4e2d'
print(ch2.encode('unicode_escape').decode('utf-8').encode('utf-8'))     # b'\\u4e2d'
print(ch2.encode('unicode_escape').decode('utf-8').encode('utf-8').decode('unicode_escape'))        # '中'
