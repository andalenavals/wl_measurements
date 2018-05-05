import os
def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='plot rho-statistics')
    
    parser.add_argument('--inputfile', default='',
                        help='Place where files with the rho measurments are')
    parser.add_argument('--outpath', default='./', 
                        help='Name of the path were the output willbe')
    parser.add_argument('--outname', default='default.png', type=str, 
                        help='Name of the output image example zone01.png , the extension is defined later')

    args = parser.parse_args()

    return args

def plot_rho_old(gg, name):
    import treecorr
    import matplotlib 
    matplotlib.use('Agg')
    import matplotlib.pylab as pl
    import numpy as np
   

    r = np.exp(gg.meanlogr)
    xip = gg.xip
    xim = gg.xim
    sig = np.sqrt(gg.varxi)

    pl.plot(r, xip, color='blue')
    pl.plot(r, -xip, color='blue', ls=':')
    pl.errorbar(r[xip>0], xip[xip>0], yerr=sig[xip>0], color='blue', lw=0.1, ls='')
    pl.errorbar(r[xip<0], -xip[xip<0], yerr=sig[xip<0], color='blue', lw=0.1, ls='')
    lp = pl.errorbar(-r, xip, yerr=sig, color='blue')

    pl.plot(r, xim, color='green')
    pl.plot(r, -xim, color='green', ls=':')
    pl.errorbar(r[xim>0], xim[xim>0], yerr=sig[xim>0], color='green', lw=0.1, ls='')
    pl.errorbar(r[xim<0], -xim[xim<0], yerr=sig[xim<0], color='green', lw=0.1, ls='')
    lm = pl.errorbar(-r, xim, yerr=sig, color='green')

    pl.xscale('log')
    pl.yscale('log', nonposy='clip')
    pl.xlabel(r'$\theta$ (arcmin)')
    pl.legend([lp, lm], [r'$\xi_+(\theta)$', r'$\xi_-(\theta)$'])
    pl.xlim( [1,500] )
    pl.ylabel(r'$\xi_{+,-}$')
    pl.savefig(name, dpi=150)
def plot_rho(gg, filename):
    import matplotlib 
    matplotlib.use('Agg')
    import matplotlib.pylab as pl
    import numpy as np

    ( meanlogr,
      rho1p,
      rho1p_im,
      rho1m,
      rho1m_im,
      var1,
    ) = gg[-1]
    
    r = np.exp(meanlogr)
    xip = np.array(rho1p)
    xim = np.array(rho1m)
    sig =  np.sqrt(var1)

    pl.plot(r, xip, color='blue',  marker='o')
    pl.plot(r, -xip, color='blue', ls=':',  marker='v')
    pl.errorbar(r[xip>0], xip[xip>0], yerr=sig[xip>0], color='blue', lw=0.1, ls='') #
    pl.errorbar(r[xip<0], -xip[xip<0], yerr=sig[xip<0], color='blue', lw=0.1, ls='')
    lp = pl.errorbar(-r, xip, yerr=sig, color='blue')

    pl.plot(r, xim, color='green', marker='o')
    pl.plot(r, -xim, color='green', ls=':', marker='v')
    pl.errorbar(r[xim>0], xim[xim>0], yerr=sig[xim>0], color='green', lw=0.1, ls='')
    pl.errorbar(r[xim<0], -xim[xim<0], yerr=sig[xim<0], color='green', lw=0.1, ls='')
    lm = pl.errorbar(-r, xim, yerr=sig, color='green')
    
    pl.xscale('log')
    pl.yscale('log', nonposy='clip')
    pl.xlabel(r'$\theta$ (arcmin)', fontsize=15)
    pl.ylabel(r'$\xi_{+,-}$', fontsize=15)
    pl.legend([lp, lm], [r'$\xi_+(\theta)$', r'$\xi_-(\theta)$'])
    pl.xlim( [1,500] )
    pl.savefig(filename, dpi=150)

def main():
    import numpy as np
    import json

    args = parse_args()

    if not os.path.isfile(args.inputfile):
        print ('File not found: ',stat_file)
        return None

    with open(args.inputfile,'r') as f:
        stats = json.load(f)

    filename =  os.path.join(args.outpath, args.outname)
    plot_rho(stats, filename)
    print('Plot was done successfully')

    
if __name__ == "__main__":
    main()
