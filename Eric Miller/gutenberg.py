#!/usr/bin/env python
import requests
import zipfile
import os

id = 84
localZip = "%s.zip" % ( id )
fileName = "%s.txt" % ( id )
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

def urlFactory():
    path = ""
    idArray = [int(i) for i in str(id)]
    del idArray[-1]
    for i in idArray:
        path += "/%s" % ( i )
    url = "http://www.gutenberg.lib.md.us%s/%s/%s.zip" % ( path, id, id )
    return url


def getZip ( zipUrl ):
    resp = requests.get( zipUrl, headers=headers, stream=True )
    with open( localZip, 'wb' ) as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def extractZip():
    zf = zipfile.ZipFile(localZip)
    data = zf.read(fileName)
    return data

def cleanUp():
    os.remove(localZip)

if __name__ == "__main__":
    zipUrl = urlFactory ()
    getZip ( zipUrl )
    data = extractZip ()
    print data
    cleanUp()
