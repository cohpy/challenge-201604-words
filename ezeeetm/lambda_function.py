#!/usr/bin/env python
import requests
import zipfile
import os
import string
import collections

def UrlFactory ( id ):
    try:
        if id <= 9:
            url = "http://www.gutenberg.lib.md.us/0/%s/%s.zip" % ( id, id )
        else:
            path = ""
            idArray = [int(i) for i in str(id)]
            del idArray[-1]
            for i in idArray:
                path += "/%s" % ( i )
            url = "http://www.gutenberg.lib.md.us%s/%s/%s.zip" % ( path, id, id )
    except:
        raise Exception ('BAD ID, PLEASE TRY AN INTEGER VALUE FOR ID...')
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
    data = zf.read(fileName)
    data = data.replace('\r\n',' ').replace('\"','').split(' ')
    data = filter(None, data)
    data = [x.lower() for x in data]
    data = [''.join(c for c in s if c not in string.punctuation) for s in data]
    return data

def WordListToFreqDict ( wordlist ):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

def SortFreqDict ( freqdict ):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux[:10]

def cleanUp ( localZip ):
    os.remove(localZip)

def lambda_handler ( event, context ):
    id = event['id']
    localZip = "/tmp/%s.zip" % ( id )

    zipUrl = UrlFactory ( id )
    GetBookTxtZip ( zipUrl, localZip )
    wordList = WordListFactory ( localZip, id )
    wordFreqList = WordListToFreqDict( wordList )
    wordFreqListSorted = SortFreqDict ( wordFreqList )
    print wordFreqListSorted

    cleanUp ( localZip )
