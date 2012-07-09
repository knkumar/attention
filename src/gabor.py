import numpy as np
import matplotlib.pyplot as plt
# To display the result (plot functions)
import matplotlib.cm as cm
# To display the result (colormaps)


def make_gabor(values, orientation, sigma=0.8):     

    vals = np.linspace(-np.pi,np.pi,values)
    # vals.shape : (100,)
    xgrid, ygrid = np.meshgrid(vals,vals)
    # xgrid.shape : (100,100)
    # ygrid.shape : (100,100)

    # Simple Gaussian : mean = 0, std = 1, amplitude = 1
    the_gaussian = 10 * np.exp( - ((xgrid/(2*sigma**2))**2 + (ygrid/(2*sigma**2))**2) )
    

    the_sine = 10 *  np.sin(xgrid * 10)
    # Simple sine wave grating : orientation = 0, phase = 0, amplitude = 1, frequency = 10/(2*pi)


    the_gabor = the_gaussian * the_sine 
    # Elementwise multiplication of Gaussian and sine wave grating
    #the_gabor = the_gabor / np.min(the_gabor)

    if orientation == "horizontal":
        return the_gabor
    else:
        return np.transpose(the_gabor)

if __name__ == "__main__":
    the_gabor = make_gabor(1000, "horizontal", 0.95)
    plt.imshow(the_gabor,cm.Greys, interpolation='nearest', vmin=-500, vmax=300) 
    plt.savefig("../images/gabor_hor.png")
    the_gabor = make_gabor(1000, "vertical", 0.95)
    plt.imshow(the_gabor,cm.Greys, interpolation='nearest', vmin=-500, vmax=300) 
    plt.savefig("../images/gabor_ver.png")
