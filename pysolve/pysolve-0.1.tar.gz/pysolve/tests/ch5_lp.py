""" Code for the LP model
"""
# pylint: disable=invalid-name
import time

from pysolve.model import Model
from pysolve.utils import round_solution, is_close


def create_lp_model():
    """ Creates model LP """
    # pylint: disable=too-many-statements
    model = Model()

    model.set_var_default(0)
    model.var('Bcb', desc='Government bills held by the Central Bank')
    model.var('Bd', desc='Demand for government bills')
    model.var('Bh', desc='Government bills held by households')
    model.var('Bs', desc='Government bills supplied by government')
    model.var('BLd', desc='Demand for government bonds')
    model.var('BLh', desc='Government bonds held by households')
    model.var('BLs', desc='Supply of government bonds')
    model.var('CG', desc='Capital gains on bonds')
    model.var('CGe', desc='Expected capital gains on bonds')
    model.var('C', desc='Consumption')
    model.var('ERrbl', desc='Expected rate of return on bonds')
    model.var('Hd', desc='Demand for cash')
    model.var('Hh', desc='Cash held by households')
    model.var('Hs', desc='Cash supplied by the central bank')
    model.var('Pbl', desc='Price of bonds')
    model.var('Pble', desc='Expected price of bonds')
    model.var('Rb', desc='Interest rate on government bills')
    model.var('Rbl', desc='Interest rate on government bonds')
    model.var('T', desc='Taxes')
    model.var('V', desc='Household wealth')
    model.var('Ve', desc='Expected household wealth')
    model.var('Y', desc='Income = GDP')
    model.var('YDr', desc='Regular disposable income of households')
    model.var('YDre', desc='Expected regular disposable income of households')

    model.set_param_default(0)
    model.param('alpha1', desc='Propensity to consume out of income')
    model.param('alpha2', desc='Propensit to consume out of wealth')
    model.param('chi', desc='Weight of conviction in expected bond price')
    model.param('lambda10', desc='Parameter in asset demand function')
    model.param('lambda12', desc='Parameter in asset demand function')
    model.param('lambda13', desc='Parameter in asset demand function')
    model.param('lambda14', desc='Parameter in asset demand function')
    model.param('lambda20', desc='Parameter in asset demand function')
    model.param('lambda22', desc='Parameter in asset demand function')
    model.param('lambda23', desc='Parameter in asset demand function')
    model.param('lambda24', desc='Parameter in asset demand function')
    model.param('lambda30', desc='Parameter in asset demand function')
    model.param('lambda32', desc='Parameter in asset demand function')
    model.param('lambda33', desc='Parameter in asset demand function')
    model.param('lambda34', desc='Parameter in asset demand function')
    model.param('theta', desc='Tax rate')

    model.param('G', desc='Government goods')
    model.param('Rbar', desc='Exogenously set interest rate on govt bills')
    model.param('Pblbar', desc='Exogenously set price of bonds')

    model.add('Y = C + G')                                  # 5.1
    model.add('YDr = Y - T + Rb(-1)*Bh(-1) + BLh(-1)')      # 5.2
    model.add('T = theta *(Y + Rb(-1)*Bh(-1) + BLh(-1))')    # 5.3
    model.add('V - V(-1) = (YDr - C) + CG')                 # 5.4
    model.add('CG = (Pbl - Pbl(-1))*BLh(-1)')
    model.add('C = alpha1*YDre + alpha2*V(-1)')
    model.add('Ve = V(-1) + (YDre - C) + CG')
    model.add('Hh = V - Bh - Pbl*BLh')
    model.add('Hd = Ve - Bd - Pbl*BLd')
    model.add('Bd = Ve*lambda20 + Ve*lambda22*Rb - ' +
              'Ve*lambda23*ERrbl - lambda24*YDre')
    model.add('BLd = (Ve*lambda30 - Ve*lambda32*Rb ' +
              ' + Ve*lambda33*ERrbl - lambda34*YDre)/Pbl')
    model.add('Bh = Bd')
    model.add('BLh = BLd')
    model.add('Bs - Bs(-1) = (G + Rb(-1)*Bs(-1) + ' +
              'BLs(-1)) - (T + Rb(-1)*Bcb(-1)) - (BLs - BLs(-1))*Pbl')
    model.add('Hs - Hs(-1) = Bcb - Bcb(-1)')
    model.add('Bcb = Bs - Bh')
    model.add('BLs = BLh')
    model.add('ERrbl = Rbl + chi * (Pble - Pbl) / Pbl')
    model.add('Rbl = 1./Pbl')
    model.add('Pble = Pbl')
    model.add('CGe = chi * (Pble - Pbl)*BLh')
    model.add('YDre = YDr(-1)')
    model.add('Rb = Rbar')
    model.add('Pbl = Pblbar')

    # if_true(x) returns 1 if x is true, else 0 is returned
    #model.add('z1 = if_true(tp > top)')
    #model.add('z2 = if_true(tp < bot)')
    return model

def create_disinf1_model():
    model = Model()

    model.set_var_default(0)
    model.var('Ck', desc='REal consumption')
    model.var('C', desc='Consumption at current prices')
    model.var('F', desc='Realized firm profits')
    model.var('Fb', desc='Realized bank profits')
    model.var('IN', desc='Stock of inventories at current costs')
    model.var('INk', desc='Real inventories')
    model.var('INke', desc='Expected real inventories')
    model.var('INkt', desc='Target level of real inventories')
    model.var('Ld', desc='Demand for loans')
    model.var('Ls', desc='Supply of loans')
    model.var('Mh', desc='Deposits held by households')
    model.var('Mhk', desc='Real alue of deposits held by households')
    model.var('Ms', desc='Supply of deposits')
    model.var('N', desc='Employment level')
    model.var('omegat', desc='Target real wage rate')
    model.var('P', desc='Price level')
    model.var('PIC', desc='Inflation rate of unit costs')
    model.var('Rl', desc='Interest rate on loans')
    model.var('Rm', desc='Interest rate on deposits')
    model.var('RRc', desc='Real interest rate on bank loans')
    model.var('S', desc='Sales at current prices')
    model.var('Sk', desc='Real sales')
    model.var('Ske', desc='Expected real sales')
    model.var('UC', desc='Unit costs')
    model.var('WB', desc='The wage bill')
    model.var('Yk', desc='Real output')
    model.var('YD', desc='Disposable income')
    model.var('YDk', desc='Real disposable income')
    model.var('YDkhs', desc='Haig-Simons measure of real disposable income')
    model.var('YDkhse', desc='Expected HS real disposable income')
    model.var('W', desc='Wage rate')

    model.set_param_default(0)
    model.param('alpha0', desc='Autonomous consumption')
    model.param('alpha1', desc='Propensity to consume out of income')
    model.param('alpha2', desc='Propensity to consume out of wealth')
    model.param('beta', desc='Parameter in expectation formations on real sales')
    model.param('eps', desc='Parameter in expectation formations on real disposable income')
    model.param('gamma', desc='Speed of adjustment of inventories to the target level')
    model.param('phi', desc='Mark-up on unit costs')
    model.param('sigmat', desc='Target inventories to sales ratio')
    model.param('omega0', desc='Exogenous component of the target real wage rate')
    model.param('omega1', desc='Relation between the target real wage rate and productivity')
    model.param('omega2', desc='Relation between the target real rate and the unemploment gap')
    model.param('omega3', desc='Speed of adjustment of the wage rate')

    model.param('ADD', desc='Spread of loans rate over the deposit rate')
    model.param('Nfe', desc='Full employment level')
    model.param('PR', desc='Labor productivity')
    model.param('Rlbar', desc='Rate of interest on bank loans, set exogenously')
    model.param('RRcbar', desc='Real interest rate on bank loans, set exogenously')


    # The production decision
    model.add('Yk = Ske + INke - INk(-1)')
    model.add('INkt = sigmat*Ske')
    model.add('INke = INk(-1) + gamma*(INkt - INk(-1))')
    model.add('INk - INk(-1) = Yk - Sk')
    model.add('Ske = beta*Sk(-1) + (1-beta)*Ske(-1)')
    model.add('Sk = Ck')
    model.add('N = Yk / PR')
    model.add('WB = N*W')
    model.add('UC = WB/Yk')
    model.add('IN = INk*UC')
    
    # The pricing decision
    model.add('S = P*Sk')
    model.add('F = S - WB + IN - IN(-1) - Rl(-1)*IN(-1)')
    model.add('P = (1 + phi)*(1+RRc*sigmat)*UC')
    
    # The banking system
    model.add('Ld = IN')
    model.add('Ls = Ld')
    model.add('Ms = Ls')
    model.add('Rm = Rl - ADD')
    model.add('Fb = Rl(-1)*Ld(-1) - Rm(-1)*Mh(-1)')
    model.add('PIC = (UC/UC(-1)) - 1')
    model.add('RRc = RRcbar')
    model.add('Rl = (1 + RRc)*(1 + PIC) - 1')
    
    # The consumption decision
    model.add('YD = WB + F + Fb + Rm(-1)*Mh(-1)')
    model.add('Mh - Mh(-1) = YD - C')
    model.add('YDkhs = Ck + (Mhk - Mhk(-1))')
    model.add('YDk = YD/P')
    model.add('C = Ck*P')
    model.add('Mhk = Mh/P')
    model.add('Ck = alpha0 + alpha1*YDkhse + alpha2*Mhk(-1)')
    model.add('YDkhse = eps*YDkhs(-1) + (1 - eps)*YDkhse(-1)')
    
    # The inflation process
    model.add('omegat = omega0 + omega1*PR + omega2*(N/Nfe)')
    model.add('W = W(-1)*(1 + omega3*omegat(-1)-(W(-1)/P(-1)))')

    return model

disinf1_parameters = {'alpha0': 15,
                      'alpha1': 0.8,
                      'alpha2': 0.1,
                      'beta': 0.9,
                      'eps': 0.8,
                      'gamma': 0.25,
                      'phi': 0.24,
                      'sigmat': 0.2,
                      'omega1': 1,
                      'omega2': 1.2,
                      'omega3': 0.3}
disinf1_exogenous = {'ADD': 0.02,
                     'PR': 1,
                     'RRcbar': 0.04}
disinf1_variables = {'Rl': (1 + 0.04) - 1,
                     'Rm': (1 + 0.04) - 1 - 0.02,
                     'W': 1,
                     'WB': 1}

def initialize_disinf1_variables(m):
    m.parameters['omega0'].value = m.evaluate('0.8 - omega1*PR - omega2')
    m.variables['UC'].value = m.evaluate('W/PR')
    m.variables['P'].value = m.evaluate('(1+phi)*(1+RRcbar*sigmat)*UC')
    m.variables['YDkhs'].value = m.evaluate('alpha0/(1-alpha1-alpha2*sigmat*UC/P)')
    m.variables['Ck'].value = m.variables['YDkhs'].value
    m.variables['Sk'].value = m.variables['Ck'].value
    m.variables['INk'].value = m.evaluate('sigmat*Sk')
    m.variables['IN'].value = m.evaluate('INk*UC')
    m.variables['Ld'].value = m.variables['IN'].value
    m.variables['Mh'].value = m.variables['Ld'].value
    m.variables['Mhk'].value = m.evaluate('Mh/P')
    m.variables['Ms'].value = m.variables['Mh'].value
    m.variables['Ls'].value = m.variables['Ld'].value
    m.variables['Ske'].value = m.variables['Sk'].value
    m.variables['YDkhse'].value = m.variables['YDkhs'].value
    m.variables['omegat'].value = m.evaluate('W/P')
    m.parameters['Nfe'].value = m.evaluate('Sk/PR')
    m.variables['Yk'].value = m.evaluate('Ske')

start = time.clock()

sim = create_lp_model()
sim.set_variables({'V': 95.803,
                   'Bh': 37.839,
                   'Bs': 57.964,
                   'Bcb': 57.964 - 37.839,
                   'BLh': 1.892,
                   'BLs': 1.892,
                   'Hs': 20.125,
                   'YDr': 95.803,
                   'Rb': 0.03,
                   'Pbl': 20})
sim.set_parameters({'alpha1': 0.8,
                    'alpha2': 0.2,
                    'chi': 0.1,
                    'lambda20': 0.44196,
                    'lambda22': 1.1,
                    'lambda23': 1,
                    'lambda24': 0.03,
                    'lambda30': 0.3997,
                    'lambda32': 1,
                    'lambda33': 1.1,
                    'lambda34': 0.03,
                    'theta': 0.1938})
sim.set_parameters({'G': 20,
                    'Rbar': 0.03,
                    'Pblbar': 20})

sim = create_disinf1_model()
sim.set_parameters(disinf1_parameters)
sim.set_parameters(disinf1_exogenous)
sim.set_variables(disinf1_variables)
initialize_disinf1_variables(sim)

for _ in xrange(100):
    sim.solve(iterations=100, threshold=1e-5)

    prev_soln = sim.solutions[-2]
    soln = sim.solutions[-1]
    if is_close(prev_soln, soln, atol=1e-3):
        break

end = time.clock()
print "elapsed time = " + str(end-start)

print round_solution(sim.solutions[-1], decimals=1)
