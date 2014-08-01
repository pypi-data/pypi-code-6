import matplotlib.pyplot as plt
import numpy.ma as ma

def plot(x, y, quantity, mask, yscale='linear'):
    """
    Plot `y` as function of `x` where `y` has quantity `quantity` and `x` is frequency :math:`f`.
    
    :param x: Array of values for the `x`-axis.
    :param y: Array of values for the `y`-axis.
    :param quantity: Quantity
    :param mask: Array of booleans.
    
    :returns: Figure.
    :type: :class:`matplotlib.figure.Figure`
    
    
    """
    x = ma.masked_array(x, mask=mask).compressed()
    y = ma.masked_array(y, mask=mask).compressed()
    
    try:
        label = ATTRIBUTES[quantity]
    except KeyError:
        label = "Unknown quantity"
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    ax.set_xscale('log')
    ax.set_yscale(yscale)
    ax.set_xlabel('$f$ in Hz')
    ax.set_ylabel(label)
    ax.grid()
    return fig

    
ATTRIBUTES = {'pressure_level'              :   '$L_p$ in dB',
              'velocity_level'              :   '$L_v$ in dB',
              'power_level'                 :   '$L_P$ in dB',
              'mass'                        :   '$m$ in kg',
              'impedance'                   :   '$Z$ in ...',
              'resistance'                  :   '$R$ in ...',
              'resistance_point_average'     :  '$R$ in ...',
              'mobility'                    :   '$Y$ in ...',
              'modal_density'               :   '$n$ in ...',
              'average_frequency_spacing'   :   '$\Delta f$ in Hz',
              'soundspeed_group'            :   '$c_{g}$ in m/s',
              'soundspeed_phase'            :   '$c_{\phi}$ in m/s',
              'clf'                         :   '$\eta$ in ...',
              'input_power'                 :   '$P$ in W',
              'loss_factor'                 :   '$\eta$ in $\mathrm{rad}^{-1}$',
              'wavenumber'                  :   '$k$ in rad/m', 
              'power'                       :   '$P$ in W',
              }
