#!/usr/bin/python

from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.io import fits
import sys
from astropy.wcs import WCS
import numpy as np

def filter_table(cat,mask,outname):

# arguments: input cat, mask fits, output cat

    t=Table.read(cat)
    mask=fits.open(mask)
    w=WCS(mask[0].header)

    pos=w.wcs_world2pix(t['RA'],t['DEC'],0,0,0)
    print len(pos)
    print mask[0].data.shape
    maxy,maxx=mask[0].data.shape
    filter=[]
    for i,r in enumerate(t):
        if (i % 1000)==0:
            print i
        x=int(pos[0][i])
        y=int(pos[1][i])
        if x<0 or y<0 or x>=maxx or y>=maxy:
            inmask=False
        else:
            inmask=~np.isnan(mask[0].data[y,x])

        filter.append(inmask)
        #print i,x,y,inmask

    t_new=t[filter]
    t_new.write(outname,overwrite=True)

if __name__=='__main__':
    filter_table(sys.argv[1],sys.argv[2],sys.argv[3])
