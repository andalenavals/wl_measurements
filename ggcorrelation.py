import os

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Read catalog program, it is assume a structure of the catalog. First the expousurelist is a column of numbers. Second each expousure have a folder. Third each folder of each expousure have a exp_info_%d.fits, which have the ccd numbers,')
    
    parser.add_argument('--explist', default='',
                        help='txt list with the number identifier of the expousure')
    parser.add_argument('--fields', nargs='+',  type=str, 
                        help='list of fields you want to read from the catalog')
    parser.add_argument('--inpath', default='./',
                        help='Place where input catalogs is, it is assumed that each expousure have a folder')
    parser.add_argument('--outpath', default='./',
                        help='Place where the output files will be sent')
    parser.add_argument('--outname', default='gg.json',
                        help='Name of the output file')

    args = parser.parse_args()

    return args

def load_explist(args):
    if args.explist != '':
        print('Read file ',args.explist)
        with open(args.explist) as fin:
            exps = [ line.strip() for line in fin if line[0] != '#' ]
        print('File includes %d exposures'%len(exps))
        exps = sorted(exps)
    else:
        print('WARNING: Not exposure list')
    return exps

def read_alldata(args):
    import fitsio
    import numpy as np
    import glob

    inpath = os.path.expanduser(args.inpath)
    if not os.path.exists(inpath):
        print('The path of the catalog does not exist!')
        return None
    #keys = args.fields
    keys = ['ra', 'dec', 's1',  's2', 'e1' ,'e2', 'kappa']
    all_data = { key : [] for key in keys }
    all_keys = keys

    if(args.explist):
        nums = load_explist(args)
        for num in nums:
            inum = int(num)
            try:
                einfo = fitsio.read(os.path.join(inpath, 'aardvarkv1.0_des_lenscat_s2n20.%d.fit'%inum))
                # print('File exp_psf_cat %d.  sucessfully read'%expnum)
            except (OSError, IOError):
                print('Unable to open aardvarkv1.0_des_lenscat_s2n20.%s.fits. Skipping it.'%inum)
                
            for key in all_keys:
                all_data[key].append(einfo[key])
        all_data_final = { key : [] for key in keys }         
        for key in all_keys:
            all_data_final[key] = np.concatenate(all_data[key])         
    else:
        files=glob.glob(os.path.join(args.inpath,'*.fit'))
        for f in files:
            try:
                einfo = fitsio.read(f)
                print('File',  f,  'sucessfully read')
            except(OSError, IOError):
                print('Unable to open: ',  f)
                                    
            for key in all_keys:
                all_data[key].append(einfo[key])
        all_data_final = { key : [] for key in keys }         
        for key in all_keys:
            all_data_final[key] = np.concatenate(all_data[key])
                                    
    return all_data_final
                   
def measure_rho(data):
    import treecorr

    ra = data['ra']
    dec = data['dec']
    e1 = data['e1']
    e2 = data['e2']
    s1 = data['s1']
    s2 = data['s2']
    kappa = data['kappa']
    g1 = [x/(1-y) for x, y in zip(s1, kappa)]
    g2 = [x/(1-y) for x, y in zip(s2, kappa)]
    
    ecat = treecorr.Catalog(ra=ra, dec=dec, ra_units='deg', dec_units='deg', g1=g1, g2=g2)
    ecat.name = 'ecat'

    '''
    min_sep = 0.5
    max_sep=300
    bin_size = 0.2
    bin_slop = 0.1
    gg = treecorr.GGCorrelation(min_sep=min_sep, max_sep=max_sep, sep_units='arcmin',
                                     bin_size=bin_size, bin_slop=bin_slop, verbose=2)
    '''
    min_sep = 1
    max_sep= 500
    nbins =  32
    gg = treecorr.GGCorrelation(min_sep=min_sep, max_sep=max_sep, nbins=nbins, sep_units='arcmin', verbose=2)

    gg.process(ecat)
    return gg
  
def write_stats(stat_file, gg):
    import json

    datainfo = [
        gg.meanlogr.tolist(),
        gg.xip.tolist(),
        gg.xip_im.tolist(),
        gg.xim.tolist(),
        gg.xim_im.tolist(),
        gg.varxi.tolist(),
    ]
        
    print('stat_file = ',stat_file)
    with open(stat_file,'w') as fp:
        json.dump([datainfo], fp)
    print('Done writing ',stat_file)


def main():
    from astropy.io import fits
    import fitsio
    import numpy as np
    import pandas
    import treecorr

    args = parse_args()

    data =  read_alldata(args)
    print('All data was read susccessfully')
    gg = measure_rho(data)
    print('Rho was measured successfully')
    filename =  os.path.join(args.outpath, args.outname)
    write_stats(filename,  gg)
    
if __name__ == "__main__":
    main()
