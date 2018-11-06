def main():
    from  classy  import  Class
    import numpy as np
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
                       'tau_reio':0.0925,
                       'non linear':  'halofit'}
    LCDM.set(common_settings)

    LCDM.compute()
    #----------------------------
    # MATTER POWER SPECTRUM
    #----------------------------
    kk = np.logspace(-4,np.log10(3) ,1000)
    Pks = [] 
    for z in [0, 0.1, 0.2, 0.4, 0.5, 1, 2]:
        Pkaux = []
        for k in kk:
            Pkaux.append(LCDM.pk(k,z))
        Pks.append(Pkaux)

    plt.figure (2)
    plt.xscale('log');plt.yscale('log');plt.xlim(kk[0],kk[-1])
    plt.xlabel(r'$k [h/\mathrm{Mpc}]$')
    plt.ylabel(r'$P(k)[\mathrm{Mpc}/h]^3$')
    plt.plot(kk ,Pks[0],'b-',color='blue' , label="z=0")
    plt.plot(kk ,Pks[1],'b-',color='green' , label="z=0.1")
    plt.plot(kk ,Pks[2],'b-',color='yellow' , label="z=0.2")
    plt.plot(kk ,Pks[3],'b-',color='red' , label="z=0.3")
    plt.plot(kk ,Pks[4],'b-',color='pink' , label="z=0.4")
    plt.plot(kk ,Pks[5],'b-',color='grey' , label="z=1")
    plt.plot(kk ,Pks[6],'b-',color='black' , label="z=2")
    plt.legend(loc='lower left',  shadow=True,  fontsize=15)
    plt.savefig('matter_PowerSpectrum.pdf', dpi=150)




if __name__ == "__main__":
    main()
