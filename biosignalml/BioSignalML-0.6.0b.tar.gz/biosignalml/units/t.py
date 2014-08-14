from pint import UnitRegistry
from pint.unit import Definition, UnitDefinition, ScaleConverter, UnitsContainer

ureg = UnitRegistry(None)

#ureg.define(Definition.from_string('day = [time]'))
ureg.define(UnitDefinition('day', None, (), ScaleConverter(1),
            reference=UnitsContainer({'[time]': 1.0}), is_base=True))

#ureg.define(Definition.from_string('year = 365*day'))
ureg.define(UnitDefinition('year', None, (), ScaleConverter(365),
            reference=UnitsContainer({'day': 1.0})))

#DimensionDefinition('[time]', None, None, None, is_base=True))
#ureg.define(DimensionDefinition('day',    None, None, ScaleConverter(1.0), is_base=True))


Q_ = ureg.Quantity

ureg.define('dog_year = 52 * day = dy')

lassie_lifespan = Q_(10, 'year')

x = lassie_lifespan.to('dog_years')

print(x)
