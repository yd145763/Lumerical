# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import imp

os.add_dll_directory("C:\\Program Files\\Lumerical\\2020a\\api\\python\\Lumapi.py")
lumapi = imp.load_source("lumapi","C:\\Program Files\\Lumerical\\2020a\\api\\python\\Lumapi.py")

Radii = [10e-9, 25e-9, 50e-9]

for i in range(len(Radii)):
    fdtd = lumapi.FDTD()

    Xsize = 240e-9
    Ysize = 240e-9
    Zsize = 240e-9

    R = float(Radii[i])

    WL_Start = 200e-9
    WL_Stop = 1000e-9

    fdtd.addfdtd()
    fdtd.set("x", 0.0)
    fdtd.set("x span", Xsize)
    fdtd.set("y", 0.0)
    fdtd.set("y span", Ysize)
    fdtd.set("z", 0.0)
    fdtd.set("z span", Zsize)

    fdtd.set("dimension", "3D")
    fdtd.set("simulation time", 500e-15)

    fdtd.set("mesh type", "uniform")
    fdtd.set("dx", 2.5e-9)
    fdtd.set("dy", 2.5e-9)
    fdtd.set("dz", 2.5e-9)

    fdtd.addtfsf()
    fdtd.set("x", 0.0)
    fdtd.set("x span", Xsize - 40e-9)
    fdtd.set("y", 0.0)
    fdtd.set("y span", Ysize - 40e-9)
    fdtd.set("z", 0.0)
    fdtd.set("z span", Zsize - 40e-9)

    fdtd.set("injection axis", "x")
    fdtd.set("wavelength start", WL_Start)
    fdtd.set("wavelength stop", WL_Stop)

    fdtd.addmovie()
    fdtd.set("x", 0.0)
    fdtd.set("x span", Xsize)
    fdtd.set("y", 0.0)
    fdtd.set("y span", Ysize)
    fdtd.set("z", 0.0)

    fdtd.addsphere()
    fdtd.set("radius", R)
    fdtd.set("material", "Au (Gold) - Johnson and Christy")

    fdtd.addpower()
    fdtd.set("name", "DFT")
    fdtd.set("monitor type", "2D Z-normal")
    fdtd.set("x", 0.0)
    fdtd.set("x span", Xsize)
    fdtd.set("y", 0.0)
    fdtd.set("y span", Ysize)
    fdtd.set("z", 0.0)

    fdtd.setglobalmonitor("frequency points", 100.)
  

    fdtd.save("goldsphere.fsp")
    fdtd.run()

    E = fdtd.getresult("DFT","E")
    Lambda = E["lambda"]
    Lambda = Lambda[:,0]

    x = E["x"]
    x = x[:,0]
    y = E["y"]
    y = y[:,0]
    z = E["z"]

    E = E["E"]

    Ex = E[:,:,0,:,0]
    Ey = E[:,:,0,:,1]
    Ez = E[:,:,0,:,2]

    Emag = np.sqrt(np.abs(Ex)**2 + np.abs(Ey)**2 + np.abs(Ez)**2)

    lambda_want = 500e-9
    index = np.argmin(np.abs(Lambda - lambda_want))

    plt.contourf(y,x,Emag[:,:,index], 100)
    plt.colorbar()
    plt.xlabel("y")
    plt.ylabel("x")
    plt.show()
    plt.close()
