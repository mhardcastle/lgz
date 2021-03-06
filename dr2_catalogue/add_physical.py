import sys
from astropy.table import Table
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
import astropy.units as u
import numpy as np
from astropy.io import fits

infile=sys.argv[1]

t=Table.read(infile)

zspec=np.where(t['zwarning_sdss']==0,t['zspec_sdss'],np.nan)
zphot=np.where(t['flag_qual']==1,t['zphot'],np.nan)
zbest=np.where(~np.isnan(zspec),zspec,zphot)
zbest=np.where(zbest<0,np.nan,zbest)

t['z_best']=zbest
z=zbest

ld=cosmo.luminosity_distance(z)
lr=4*1e-29*np.pi*t['Total_flux']*ld.to(u.m)**2.0*(1+z)**(-0.3)
angs=cosmo.kpc_proper_per_arcmin(z)*(u.arcmin/60.0)
asize=np.where(t['LGZ_Size']>0,t['LGZ_Size'],2*t['DC_Maj'])
size=angs*asize/u.kpc
t['Size']=size
t['L_144']=lr

# Add some column descriptions

lines=open('../README.md').readlines()
for l in lines:
    if '|' not in l:
        continue
    if 'Column' in l:
        continue
    bits=l.split('|')
    if len(bits)>1:
        c=bits[1].lstrip().rstrip()
        u=bits[2].lstrip().rstrip()
        d=bits[3].lstrip().rstrip()
        if c[0]==':': continue
        t[c].description=d
        t[c].units=u

outname=infile.replace('.fits','-physical.fits')
t.write(outname,overwrite=True)

# Now work round astropy's inability to write comments into FITS tables, sigh

hdu=fits.open(outname)

nf=hdu[1].header['TFIELDS']
for i in range(1,nf+1):
    c=hdu[1].header['TTYPE%i' %i]
    hdu[1].header['TCOMM%i' %i]=t[c].description
    hdu[1].header['TUNIT%i' %i]=t[c].units

hdu.writeto(outname,overwrite=True)

                       


        
