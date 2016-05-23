#!/usr/bin/env python
import requests
import zipfile
import os
import string
import collections
import re
import boto3
import json

def UrlFactory ( id ):
    try:
        if id <= 9:
            path = '/0'
        else:
            path = ""
            idArray = [int(i) for i in str(id)]
            del idArray[-1]
            for i in idArray:
                path += "/%s" % ( i )
        url = "http://www.gutenberg.lib.md.us%s/%s/%s.zip" % ( path, id, id )
    except:
        raise Exception ('BAD ID, PLEASE TRY AN INTEGER VALUE FOR ID...')
	print ( url )
    return url

def GetBookTxtZip ( zipUrl, localZip ):
    resp = requests.get( zipUrl, stream=True )
    with open( localZip, 'wb' ) as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def WordListFactory ( localZip, id ):
    fileName = "%s.txt" % ( id )
    zf = zipfile.ZipFile(localZip)
    wordList = zf.read(fileName)
    wordList = wordList.replace('\r\n',' ').replace('\"','').split(' ')
    wordList = filter(None, wordList)
    wordList = [word.lower() for word in wordList]
    wordList = [''.join(c for c in word if c not in string.punctuation) for word in wordList]
    return wordList

def WordListToFreqDict ( wordlist ):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

def SortFreqDict ( freqdict ):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux[:10]

def Test ( results ):
    """This function tests that words in result sets satisfy the definition in README.md

    >>> Test('word')
    True
    >>> Test('This-Word')
    if you got word problems I feel bad for you son. I got 99 problems, but " This-Word " aint one: Exception
    Traceback (most recent call last):
    File "/var/task/lambda_function.py", line 73, in lambda_handler
    Test ( wordFreqListSorted ) File "/var/task/lambda_function.py", line 57, in Test
    raise Exception (exception)
    Exception: if you got word problems I feel bad for you son. I got 99 problems, but " This-Word " aint one
    """
    for resultSet in results:
        word = resultSet[1]
        matchObj = re.match( r'\b[a-z]+\b', word)
        if matchObj is None:
            exception = "if you got word problems I feel bad for you son.  I got 99 problems, but \" %s \" aint one" % ( word )
            raise Exception (exception)
    return True

def UploadToS3 ( id, wordFreqList ):
    s3 = boto3.resource('s3')
    bucket = 'gutenberg-out'
    key = "%s.json" % ( id )
    body = json.dumps(wordFreqList)
    s3.Object(bucket, key).put(Body=body)

def CleanUp ( localZip ):
    os.remove(localZip)

def lambda_handler ( event, context ):
	id = event['id']
	localZip = "/tmp/%s.zip" % ( id )
	print(id)
	print(localZip)
	
	zipUrl = UrlFactory ( id )
	GetBookTxtZip ( zipUrl, localZip )
	wordList = WordListFactory ( localZip, id )
	wordFreqList = WordListToFreqDict( wordList )
	wordFreqListSorted = SortFreqDict ( wordFreqList )
	Test ( wordFreqListSorted )
	UploadToS3 (id, wordFreqList )
	
	print wordFreqListSorted
	CleanUp ( localZip )