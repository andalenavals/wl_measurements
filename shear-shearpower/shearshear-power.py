import numpy as np

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Read catalog program format h5')
    
    #parser.add_argument('--psf_cat', default='/home2/dfa/sobreira/alsina/catalogs/y3_master/Y3_mastercat_v1_6_20_18_subsampled.h5',
    #                    help='Full Path to the catalog')
    parser.add_argument('--psf_cat', default='/data/catalogs/y3_master/Y3_mastercat_v1_6_20_18_subsampled.h5',
                        help='Full Path to the catalog')
 

    args = parser.parse_args()

    return args


#radial comoving distance in Mpc
def chi(z1, z2 , pars):
    import numpy as np
    from scipy.integrate import quad
    h = pars[1]
    Omegas = pars[2:]
    def Integrand(z, Omegas):
        import numpy as np
        E =  np.sqrt( (1 - Omegas[0] - Omegas[1] - Omegas[2] ) + Omegas[0] * np.power(1 + z, 3) + Omegas[1] * np.power(1 + z, 4 ) + Omegas[2] )
        return 1. / E
    I,e = quad(Integrand, z1, z2,  args=(Omegas))
    return 3000 * I / h
    
#comoving angular diameter distance in Mpc
def S(z,  pars):
    X = chi(0, z,  pars)
    K = pars[0] 
    if (K==0):
        return X
    elif (K>0):
        sk = np.sqrt(K)
        return np.sinh(sk * X) / sk
    else:
        skk =  np.sqrt(-K)
        return np.sin(skk * X) / skk

#Photometric redshift distribution
def p1(z):
    mu, sig = 1.0 ,  0.15
    return np.exp(-np.power(z - mu, 2.) / (2 * np.power(sig, 2.)))

#Lensing efficiency
def g(z1,pars, red_dist):
    import numpy as np
    from scipy.integrate import quad
    def Integrand2(zl):
        #print("   MONDAA")
        #print("   redshift", red_dist(zl))
        #print("   Comoving radial", S(zl - z1, pars)  ) 
        return red_dist(zl)*S(zl - z1, pars)/S(zl, pars) 
    z_hor = 1089
    h = pars[1]
    Om =  pars[2]
    Pf =  1.5 *((h / 3000.)**2)*(1 + z1)*Om * S(z1, pars)
    #print("puto z",  z1)
    #print("Puto S", S(z1, pars))
    print("Puto Pf", Pf)
    I,e = quad(Integrand2, z1, z_hor)
    print("Puto I", I)
    return Pf * I
##Shear-Shear Power spectrum
def Pgg(l, red_dist1, red_dist2,  Pm, pars):
    from scipy.integrate import quad
    def Integrand(z):
        return g(z, pars,red_dist1) * g(z, pars,red_dist2) * Pm(l /S(z, pars) , z) / (S(z, pars) ** 2)
    z_hor = 1089
    I,e = quad(Integrand, 0, z_hor)
    #print("Puto lensing efficiency", g(0.1, pars,red_dist1))
    return I
    
def main():
    from  classy  import  Class
    import matplotlib.pyplot as plt

    # create instance of the class "Class"
    LCDM = Class()
    # pass input parameters
    common_settings = {'output' : 'mPk',
                       'z_pk': 1089, 
                       'P_k_max_1/Mpc':3.0, 
                       # LambdaCDM parameters
                       'h':0.67556,
                       'omega_b':0.022032,
                       'omega_cdm':0.12038,
                       'A_s':2.215e-9,
                       'n_s':0.9619,
                       'tau_reio':0.0925}
    LCDM.set(common_settings)
    #LCDM.set({'output':'mPk','lensing':'no','P_k_max_1/Mpc':3.0})
    # run class
    
    #LCDM.compute()

    #-----------------------------------------------------------------------------
    # SHEAR-SHEAR POWER SPECTRUM
    #-----------------------------------------------------------------------------
    pars = []
    pars.append(0) #curvature
    pars.append(0.67556)
    pars.append(0.27)#Omega_m
    pars.append(8.24e-5) #Omega_r
    pars.append(0.73) #Omega L
    print(pars)

    #Pgg(1000, p1,  p1, LCDM.pk , pars)
    '''
    #Shear Power spectrum
    ll = np.logspace(-1, 4 ,10)
    Pg = []
    for l in ll:
        #print(Pgg(l, p1,  p1, LCDM.pk , pars))
        Pg.append(Pgg(l, p1,  p1, LCDM.pk , pars) )
    plt.figure(1)
    plt.xscale('log');plt.yscale('log');plt.xlim(ll[0],ll[-1])
    plt.xlabel(r'$l$')
    plt.ylabel(r'$P(l)[\mathrm{Mpc}/h]^3$')
    plt.plot(ll ,Pg,'b-')
    plt.savefig('shear_PowerSpectrum1.pdf', dpi=150)
    print(ll)
    print(Pg)
    '''

    '''
    #Comoving radial distance
    zz = np.logspace(-1,1,1000)
    D = []
    for z in zz:
        D.append( S(z,  pars))
    plt.figure (2)
    plt.xscale('log');plt.yscale('log');plt.xlim(zz[0],zz[-1])
    plt.xlabel(r'z')
    plt.ylabel(r'D')
    plt.plot(zz ,D,'b-')
    plt.savefig('Distance.pdf', dpi=150)
    '''
    
    
    # Photometric redshiftdistribution
    '''
    zz = np.linspace(0,2.0,1000)
    PRS = []
    for z in zz:
        PRS.append( p1(z))
    plt.figure (3)
    #plt.xscale('log');plt.yscale('log');plt.xlim(zz[0],zz[-1])
    plt.xlabel(r'z')
    plt.ylabel(r'p(z)')
    plt.plot(zz ,PRS,'b-')
    plt.savefig('Photometric_redshidt_distribution.pdf', dpi=150)
    '''

    g(0.8, pars, p1)
    '''
    ##Lensing efficiency
    zz = np.linspace(0,2.0,10)
    PRS = []
    for z in zz:
        PRS.append( g(z, pars, p1) )
    plt.figure (3)
    #plt.xscale('log');plt.yscale('log');plt.xlim(zz[0],zz[-1])
    plt.xlabel(r'z')
    plt.ylabel(r'p(z)')
    plt.plot(zz ,PRS,'b-')
    plt.savefig('Lensing_eficiency.pdf', dpi=150)
    '''
    

    

if __name__ == "__main__":
    main()
