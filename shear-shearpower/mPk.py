def main():
    from  classy  import  Class
    import numpy as np
    import matplotlib.pyplot as plt

    # create instance of the class "Class"
    LCDM = Class()
    # pass input parameters
    common_settings = {'output' : 'mPk',
                       'P_k_max_1/Mpc':3.0, 
                       # LambdaCDM parameters
                       'h':0.67556,
                       'omega_b':0.022032,
                       'omega_cdm':0.12038,
                       'A_s':2.215e-9,
                       'n_s':0.9619,
                       'tau_reio':0.0925}
    LCDM.set(common_settings)

    LCDM.compute()
    #----------------------------
    # MATTER POWER SPECTRUM
    #----------------------------
    kk = np.logspace(-4,np.log10 (3) ,1000)
    Pk = []
    for k in kk:
        Pk.append(LCDM.pk(k,0.))

    plt.figure (2)
    plt.xscale('log');plt.yscale('log');plt.xlim(kk[0],kk[-1])
    plt.xlabel(r'$k [h/\mathrm{Mpc}]$')
    plt.ylabel(r'$P(k)[\mathrm{Mpc}/h]^3$')
    plt.plot(kk ,Pk,'b-')
    plt.savefig('matter_PowerSpectrum.pdf', dpi=150)




if __name__ == "__main__":
    main()
