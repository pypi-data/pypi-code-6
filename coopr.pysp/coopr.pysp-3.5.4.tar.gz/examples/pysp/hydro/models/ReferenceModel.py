# started as elec3 from Pierre on 8 Dec 2010; removed scenarios
#
# Imports
#
from coopr.pyomo import *

##
## Setting up a Model
##
#
# Create the model
#
model = AbstractModel()
model.name="elec3"
#
# Create sets used to define parameters
#

### etaps

model.nb_etap=Param(within=PositiveIntegers)

model.etap = RangeSet(1,model.nb_etap)

##
## Declaring Params
##
#
model.A=Param(model.etap)
model.D=Param(model.etap)

model.betaGt=Param()
model.betaGh=Param()
model.betaDns=Param()

model.PgtMax=Param()
model.PgtMin=Param()
model.PghMin=Param()
model.PghMax=Param()

model.VMin=Param()
model.VMax=Param()

model.u=Param(model.etap)
model.duracion=Param(model.etap)
model.V0=Param()
model.T=Param()


#bounds and variables

def Pgt_bounds(model, t):
    return(model.PgtMin,model.PgtMax)
model.Pgt = Var(model.etap, bounds=Pgt_bounds, within=NonNegativeReals)

def Pgh_bounds(model, t):
    return(model.PghMin,model.PghMax)
model.Pgh = Var(model.etap, bounds=Pgh_bounds, within=NonNegativeReals)

def PDns_bounds(model, t):
    return(0,model.D[t])
model.PDns = Var(model.etap, bounds=PDns_bounds, within=NonNegativeReals)

def Vol_bounds(model, t):
    return(model.VMin,model.VMax)
model.Vol = Var(model.etap, bounds=Vol_bounds, within=NonNegativeReals)

model.sl = Var(within=NonNegativeReals)

model.StageCost = Var(model.etap, within=Reals)

def discount_rule(model, t):
    return (1/1.1)**(value(model.duracion[t])/value(model.T))
model.r = Param(model.etap,initialize=discount_rule)


# objective

def StageCostRule(model, t):
    if t < value(model.nb_etap):
        return model.StageCost[t] == model.r[t] * (model.betaGt * model.Pgt[t] + \
                                     model.betaGh * model.Pgh[t] + \
                                     model.betaDns * model.PDns[t] )
    else:
        return model.StageCost[t] == (model.r[t] * (model.betaGt * model.Pgt[t] + \
                                     model.betaGh * model.Pgh[t] + \
                                     model.betaDns * model.PDns[t]) + model.sl)

model.StageCostConstraint = Constraint(model.etap, rule=StageCostRule)

# constraints

def fixpgh_rule(model):
    return model.Pgh[1] == 60
#model.testfixing = Constraint(rule=fixpgh_rule)

def demand_rule(model, t):
    return model.Pgt[t]+model.Pgh[t]+model.PDns[t]-model.D[t] == 0.0
model.demand= Constraint(model.etap, rule=demand_rule)

def conserv_rule(model, t):
    if t == 1:
        return model.Vol[t]-model.V0 <= model.u[t] *(model.A[t]-model.Pgh[t])
    else:
        return model.Vol[t]-model.Vol[t-1] <= model.u[t] *(model.A[t]-model.Pgh[t])
model.conserv= Constraint(model.etap, rule=conserv_rule)

def fcfe_rule(model):
    return model.sl>= 4166.67*(model.V0-model.Vol[3])
model.fcfe= Constraint(rule=fcfe_rule)


#
# PySP Auto-generated Objective
#
# minimize: sum of StageCostVariables
#
# A active scenario objective equivalent to that generated by PySP is
# included here for informational purposes.
def total_cost_rule(model):
    return summation(model.StageCost)
model.Objective_rule = Objective(rule=total_cost_rule, sense=minimize)

