import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import imp
from matplotlib.ticker import StrMethodFormatter

os.add_dll_directory("C:\\Program Files\\Lumerical\\v222\\api\\python\\lumapi.py") #the lumapi.py path in your pc, remember the double \\
lumapi = imp.load_source("lumapi","C:\\Program Files\\Lumerical\\v222\\api\\python\\lumapi.py") #the lumapi.py path in your pc, remember the double \\

fdtd = lumapi.FDTD(r"C:\Users\Lim Yudian\Documents\AMF 2022 oct tape out\Grating coupler\grating_coupler_3D.fsp")




height = 10e-6, 20e-6, 30e-6, 40e-6, 50e-6, 60e-6, 70e-6

for h in height:
    fdtd.addpower()
    fdtd.set("name", str(h))
    fdtd.set("monitor type", "2D Z-normal")
    fdtd.set("x min", -30e-6)
    fdtd.set("x max", 150e-6)
    fdtd.set("y min", -20e-6)
    fdtd.set("y max", 20e-6)
    fdtd.set("z", h)
    
fdtd.addpower()
fdtd.set("name", "y_normal")
fdtd.set("monitor type", "2D Y-normal")
fdtd.set("x min", -30e-6)
fdtd.set("x max", 150e-6)
fdtd.set("z min", -5e-6)
fdtd.set("z max", 75e-6)
fdtd.set("y", 0.0)

    
fdtd.select("FDTD")
fdtd.set("dimension", "3D")
fdtd.set("x min", -35e-6)
fdtd.set("x max", 155e-6)
fdtd.set("y min", -25e-6)
fdtd.set("y max", 25e-6)
fdtd.set("z min", -5e-6)
fdtd.set("z max", 75e-6)


fdtd.select("FDTD::ports"); # select the port group
fdtd.set("source port","port 2")
fdtd.set("source mode","mode 1")

fdtd.setglobalsource("wavelength start",1092e-9)



GDSs = "grating012umpitch05dutycycle15um", "grating012umpitch05dutycycle20um", "grating012umpitch05dutycycle30um", "grating012umpitch05dutycycle40um", "grating012umpitch05dutycycle50um", "grating012umpitch05dutycycle60um"
    
for g in GDSs:
    fdtd.gdsimport(r"C:\Users\Lim Yudian\Downloads\grating of different radius.GDS", g, 54, "Si3N4 (Silicon Nitride) - Phillip", 0, 1e-6)
    fdtd.set("name", "meow")
    fdtd.set("z span", 0.4e-6)
    fdtd.set("z", 0.1)
    fdtd.set("x", -29e-6)
    fdtd.set("y", -9e-6)
    fdtd.set("z", 0.2e-6)

    fdtd.run()
    for h in height:
        E = fdtd.getresult(str(h),"E")
        E2 = E["E"]
        Ex1 = E2[:,:,0,0,0]
        Ey1 = E2[:,:,0,0,1]
        Ez1 = E2[:,:,0,0,2]
        Emag1 = np.sqrt(np.abs(Ex1)**2 + np.abs(Ey1)**2 + np.abs(Ez1)**2)
        Emag1 = np.transpose(Emag1)
        Emag1_df = pd.DataFrame(Emag1)
        Emag1_df.to_excel('C:\\Users\\Lim Yudian\\Downloads\\'+str(h)+g+'.xlsx', index=False)
        x1 = E["x"]
        x1 = x1[:,0]
        x1 = [i*1000000 for i in x1]
        y1 = E["y"]
        y1 = y1[:,0]
        y1 = [j*1000000 for j in y1]
        z1 = E["z"]
        colorbarmax = max(Emag1.max(axis=1))
    
        fig,ax=plt.subplots(1,1)
        cp=ax.contourf(x1,y1,Emag1, 200, zdir='z', offset=-100, cmap='hot')
        clb=fig.colorbar(cp, ticks=(np.arange(0,colorbarmax,0.2)).tolist())
        clb.ax.set_title('Electric Field (eV)', fontweight="bold")
        for l in clb.ax.yaxis.get_ticklabels():
            l.set_weight("bold")
            l.set_fontsize(12)
        ax.set_xlabel('x-position (µm)', fontsize=13, fontweight="bold", labelpad=1)
        ax.set_ylabel('y-position (µm)', fontsize=13, fontweight="bold", labelpad=1)
        ax.xaxis.label.set_fontsize(13)
        ax.xaxis.label.set_weight("bold")
        ax.yaxis.label.set_fontsize(13)
        ax.yaxis.label.set_weight("bold")
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.set_yticklabels(ax.get_yticks(), weight='bold')
        ax.set_xticklabels(ax.get_xticks(), weight='bold')
        ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
        plt.show()
        plt.close()
    
    Ey = fdtd.getresult("y_normal","E")
    E2y = Ey["E"]
    Ex1y = E2y[:,0,:,0,0]
    Ey1y = E2y[:,0,:,0,1]
    Ez1y = E2y[:,0,:,0,2]
    Emag1y = np.sqrt(np.abs(Ex1y)**2 + np.abs(Ey1y)**2 + np.abs(Ez1y)**2)
    Emag1y = np.transpose(Emag1y)
    Emag1y_df = pd.DataFrame(Emag1y)
    Emag1y_df.to_excel('C:\\Users\\Lim Yudian\\Downloads\\y_'+g+'.xlsx', index=False)
    x1y = Ey["x"]
    x1y = x1y[:,0]
    x1y = [i*1000000 for i in x1y]
    z1y = Ey["z"]
    z1y = z1y[:,0]
    z1y = [j*1000000 for j in z1y]
    y1y = E["y"]
    colorbarmax = max(Emag1y.max(axis=1))
    
    fig,ax=plt.subplots(1,1)
    cp=ax.contourf(x1y,z1y,Emag1y, 200, zdir='z', offset=-100, cmap='hot')
    clb=fig.colorbar(cp, ticks=(np.arange(0,colorbarmax,0.2)).tolist())
    clb.ax.set_title('Electric Field (eV)', fontweight="bold")
    for l in clb.ax.yaxis.get_ticklabels():
        l.set_weight("bold")
        l.set_fontsize(12)
    ax.set_xlabel('x-position (µm)', fontsize=13, fontweight="bold", labelpad=1)
    ax.set_ylabel('y-position (µm)', fontsize=13, fontweight="bold", labelpad=1)
    ax.xaxis.label.set_fontsize(13)
    ax.xaxis.label.set_weight("bold")
    ax.yaxis.label.set_fontsize(13)
    ax.yaxis.label.set_weight("bold")
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.set_yticklabels(ax.get_yticks(), weight='bold')
    ax.set_xticklabels(ax.get_xticks(), weight='bold')
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
    plt.show()
    plt.close()
    
    fdtd.switchtolayout()
    
    fdtd.select("meow")
    fdtd.delete()
    








