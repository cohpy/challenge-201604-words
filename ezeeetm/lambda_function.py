#!/usr/bin/env python
import requests
import zipfile
import os
import string

def urlFactory ( id ):
    path = ""
    if id <= 9:
        url = "http://www.gutenberg.lib.md.us/0/%s/%s.zip" % ( id, id )
    else:
        idArray = [int(i) for i in str(id)]
        del idArray[-1]
        for i in idArray:
            path += "/%s" % ( i )
        url = "http://www.gutenberg.lib.md.us%s/%s/%s.zip" % ( path, id, id )
    return url

def getZip ( zipUrl, localZip ):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    resp = requests.get( zipUrl, headers=headers, stream=True )
    with open( localZip, 'wb' ) as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def extractData ( localZip, id ):
    fileName = "%s.txt" % ( id )
    zf = zipfile.ZipFile(localZip)
    data = zf.read(fileName)
    data = data.replace('\r\n',' ').replace('\"','').split(' ')
    data = filter(None, data)
    data = [x.lower() for x in data]
    data = [''.join(c for c in s if c not in string.punctuation) for s in data]
    return data

def wordListToFreqDict ( wordlist ):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

def sortFreqDict ( freqdict ):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def cleanUp ( localZip ):
    os.remove(localZip)

def lambda_handler ( event, context ):
    id = event['id']
    localZip = "/tmp/%s.zip" % ( id )

    zipUrl = urlFactory ( id )
    getZip ( zipUrl, localZip )
    data = extractData ( localZip, id )
    wordFreqList = wordListToFreqDict( data )
    wordFreqListSorted = sortFreqDict ( wordFreqList )
    print wordFreqListSorted

    cleanUp ( localZip )
