#!/usr/bin/env python
import os,re,glob,gc




def write_fit(data, file_name):
    import fitsio
    print("Writing data to ",file_name)
    fitsio.write(file_name, data.to_records(index=False), clobber=True)
        
def main():
    from astropy.io import fits
    import pandas
    import numpy as np


    zbins=[0.1,0.359677,0.543333,0.72700,0.942333,2]
    match_string='*.fit'
    dir='/home2/dfa/sobreira/alsina/catalogs/bbc/'
    outdir='/home2/dfa/sobreira/alsina/catalogs/bbc-split/'
    files=glob.glob(os.path.join(dir,match_string))
    #print(files)

    for i,file in enumerate(files):

        print 'Reading '+file
        try:
             hdus=  fits.open(file)
             dataz = hdus[1].data['z']
        except:
            print "Can't read file "+file+" skipping"
            continue

        for bin in range(0,len(zbins)-1):
            mask_zmin= dataz>zbins[bin]
            mask_zmax= dataz<zbins[bin+1]

            # add the masks together
            #boolean 
            mask=np.array([m1&m2 for m1,m2 in zip(mask_zmin,mask_zmax)])
            
            new_data=hdus[1].data[mask]
            new_data = new_data.astype(new_data.dtype.newbyteorder('='))
            df1 = pandas.DataFrame(new_data)
            basename=os.path.basename(file)
            filename=basename.replace('.fit','_%0.2f_%0.2f.fit'%(zbins[bin],zbins[bin+1]))
            outpath =os.path.join(outdir,filename)
            print ('Creating '+filename)
            write_fit(df1, outpath)   

if __name__ == "__main__":
    main()
    
