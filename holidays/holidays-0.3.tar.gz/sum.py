import holidays

bc = holidays.CA(prov='BC', years=[2013])
on = holidays.CA(prov='ON', years=[2014])
us = holidays.US()

ca = bc + on + us
