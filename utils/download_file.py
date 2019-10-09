#!/usr/bin/python
# Generic file download with retry and check for length

import requests
import os
from time import sleep

def download_file(url,filename):
    if os.path.isfile(filename):
        print 'File',filename,'already exists, skipping'
        return
    else:
        print 'Downloading',filename

    downloaded=False
    while not downloaded:
        connected=False
        while not connected:
            try:
                print 'Opening connection'
                response = requests.get(url, stream=True,verify=False,timeout=60)
                if response.status_code!=200:
                    print response.headers
                    raise RuntimeError('Code was %i' % response.status_code)
                esize=long(response.headers['Content-Length'])
            except (requests.exceptions.ConnectionError,requests.exceptions.Timeout,requests.exceptions.ReadTimeout):
                print 'Connection error! sleeping 30 seconds before retry...'
                sleep(30)
            else:
                connected=True
        try:
            print 'Downloading %i bytes' % esize
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        fd.write(chunk)
            fsize=os.path.getsize(filename)
            if esize!=fsize:
                print 'Download incomplete (expected %i, got %i)! Retrying' % (esize, fsize)
            else:
                print 'Download successful, %i of %i bytes received' % (fsize, esize)
                downloaded=True

        except requests.exceptions.ConnectionError,requests.exceptions.Timeout:
            print 'Connection error! sleeping 30 seconds before retry...'
            sleep(30) # back to the connection


    del response
