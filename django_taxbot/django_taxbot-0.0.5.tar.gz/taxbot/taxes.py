from decimal import Decimal
from django.db import models

CURRENCY_DICT = {
	'CA': 'CAD',
	'US': 'USD',
	'NG': 'NGN',
	'GB': 'GBP'
}

# Countries with Simple Taxes
SIMPLE_TAX_COUNTRIES = {
	'GB': 'GREAT BRITAIN',
	'NG': 'NIGERIA'
}

# Countries which do not have their 
# taxes broken up by city. Do not include 
# a country in this list of it is also a 
# simple tax country
NON_CITY_COUNTRIES = {
	'CA': 'CANADA'
}

TAXES = {
	'CA': {
		'DEFAULT': Decimal('0.05'), # Federal Goods and Services Tax
		# GST => Goods and Services Tax
		# HST => Harmonized Sales Tax
		# PST => Provincial Sales Tax
		# QST => Quebec Sales Tax
		# RST => Retail Sales Tax
		'AB': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None,
			}
		},
		'BC': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': Decimal('0.07'),
				'HST': None
			}
		},
		'MB': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': Decimal('0.08') # Also Provincial Sales Tax
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': Decimal('0.08'),
				'HST': None
			}
		},
		'NB': {
			'MEALS': {
				'GST': None,
				'HST': Decimal('0.13'),
				'PST': None
			},
			'SALES': {
				'GST': None,
				'PST': None,
				'HST': Decimal('0.14')
			}
		},
		'NL': {
			'MEALS': {
				'GST': None,
				'HST': Decimal('0.13'),
				'PST': None
			},
			'SALES': {
				'GST': None,
				'PST': None,
				'HST': Decimal('0.13')
			}
		},
		'NS': {
			'MEALS': {
				'GST': None,
				'HST': Decimal('0.15'),
				'PST': None
			}
		},
		'NU': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': None,
				'HST': None
			}
		},
		'NT': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': None,
				'HST': None
			}
		},
		'ON': {
			'MEALS': { # Exception for meals under $4. Then effective tax rate is only 5%
				'GST': None,
				'HST': Decimal('0.13'),
				'PST': None
			},
			'SALES': {
				'GST': None,
				'PST': None,
				'HST': Decimal('0.13')
			}
		},
		'PE': {
			'MEALS': {
				'GST': None,
				'HST': Decimal('0.14'),
				'PST': None
			},
			'SALES': {
				'GST': None,
				'PST': None,
				'HST': Decimal('0.14')
			}
		},
		'QC': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'PST': Decimal('0.075'), # Also Quebec Sales Tax
				'HST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': Decimal('0.09975'),
				'HST': None
			}
		},
		'SK': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': Decimal('0.05'),
				'HST': None
			}
		},
		'YT': {
			'MEALS': {
				'GST': Decimal('0.05'),
				'HST': None,
				'PST': None
			},
			'SALES': {
				'GST': Decimal('0.05'),
				'PST': None,
				'HST': None
			}
		}
	},
	'US': {
		'AZ': {
			'PHOENIX': {
				'MEALS': Decimal('0.093'),
				'SALES': Decimal('0.093')
			},
			'TUCSON': {
				'MEALS': Decimal('0.091'),
				'SALES': Decimal('0.091')
			},
			'MESA': {
				'MEALS': Decimal('0.0905'),
				'SALES': Decimal('0.0905')
			}
		},
		'CA': {
			'SAN DIEGO': {
				'MEALS': Decimal('0.0775'),
				'SALES': Decimal('0.0775')
			},
			'SAN JOSE': {
				'MEALS': Decimal('0.0850'),
				'SALES': Decimal('0.0825')
			},
			'SAN FRANCISCO': {
				'MEALS': Decimal('0.0850'),
				'SALES': Decimal('0.0850')
			},
			'FRESNO': {
				'MEALS': Decimal('0.07975'),
				'SALES': Decimal('0.07975')
			},
			'SACRAMENTO': {
				'MEALS': Decimal('0.0775'),
				'SALES': Decimal('0.0775')
			},
			'LONG BEACH': {
				'MEALS': Decimal('0.0875'),
				'SALES': Decimal('0.0875')
			},
			'LOS ANGELES': {
				'MEALS': Decimal('0.0875'),
				'SALES': Decimal('0.0875')
			},
			'OAKLAND': {
				'MEALS': Decimal('0.0875'),
				'SALES': Decimal('0.0875')
			}
		},
		'CO': {
			'DENVER': {
				'MEALS': Decimal('0.081'),
				'SALES': Decimal('0.041')
			},
			'COLORADO SPRINGS': {
				'MEALS': Decimal('0.074'),
				'SALES': Decimal('0.074')
			}
		},
		'DC': {
			'WASHINGTON': {
				'MEALS': Decimal('0.10'),
				'SALES': Decimal('0.06')
			}
		},
		'FL': {
			'JACKSONVILLE': {
				'MEALS': Decimal('0.09'),
				'SALES': Decimal('0.07')
			},
			'MIAMI': {
				'MEALS': Decimal('0.09'),
				'SALES': Decimal('0.07')
			}
		},
		'GA': {
			'ATLANTA': {
				'MEALS': Decimal('0.08'),
				'SALES': Decimal('0.08')
			}
		},
		'IL': {
			'CHICAGO': {
				'MEALS': Decimal('0.1075'),
				'SALES': Decimal('0.095')
			}
		},
		'IN': {
			'INDIANAPOLIS': {
				'MEALS': Decimal('0.09'),
				'SALES': Decimal('0.07')
			}
		},
		'KS': {
			'WICHITA': {
				'MEALS': Decimal('0.093'),
				'SALES': Decimal('0.093')
			}
		},
		'KY': {
			'LOUISVILLE': {
				'MEALS': Decimal('0.06'),
				'SALES': Decimal('0.06')
			}
		},
		'MA': {
			'BOSTON': {
				'MEALS': Decimal('0.07'),
				'SALES': Decimal('0.0625')
			}
		},
		'MD': {
			'BALTIMORE': {
				'MEALS': Decimal('0.06'),
				'SALES': Decimal('0.06')
			}
		},
		'MI': {
			'DETROIT': {
				'MEALS': Decimal('0.06'),
				'SALES': Decimal('0.06')
			}
		},
		'MN': {
			'MINNEAPOLIS': {
				'MEALS': Decimal('0.10775'),
				'SALES': Decimal('0.0775')
			}
		},
		'MO': {
			'KANSAS CITY': {
				'MEALS': Decimal('0.0908'),
				'SALES': Decimal('0.0785')
			}
		},
		'NC': {
			'CHARLOTTE': {
				'MEALS': Decimal('0.09'),
				'SALES': Decimal('0.08')
			},
			'RALEIGH': {
				'MEALS': Decimal('0.0775'),
				'SALES': Decimal('0.0675')
			}
		},
		'NE': {
			'OMAHA': {
				'MEALS': Decimal('0.07'),
				'SALES': Decimal('0.095')
			}
		},
		'NM': {
			'ALBUQUERQUE': {
				'MEALS': Decimal('0.069995'),
				'SALES': Decimal('0.069995')
			}
		},
		'NV': {
			'LAS VEGAS': {
				'MEALS': Decimal('0.081'),
				'SALES': Decimal('0.081')
			}
		},
		'NY': {
			'NEW YORK CITY': {
				'MEALS': Decimal('0.08875'),
				'SALES': Decimal('0.08875')
			}
		},
		'OH': {
			'COLUMBUS': {
				'MEALS': Decimal('0.0675'),
				'SALES': Decimal('0.0675')
			},
			'CLEVELAND': {
				'MEALS': Decimal('0.0775'),
				'SALES': Decimal('0.0775')
			}
		},
		'OK': {
			'OKLAHOMA CITY': {
				'MEALS': Decimal('0.08375'),
				'SALES': Decimal('0.08375')
			},
			'TULSA': {
				'MEALS': Decimal('0.075'),
				'SALES': Decimal('0.075')
			}
		},
		'OR': {
			'PORTLAND': {
				'MEALS': Decimal('0.00'),
				'SALES': Decimal('0.00')
			}
		},
		'PA': {
			'PHILADELPHIA': {
				'MEALS': Decimal('0.08'),
				'SALES': Decimal('0.08')
			}
		},
		'TN': {
			'MEMPHIS': {
				'MEALS': Decimal('0.0925'),
				'SALES': Decimal('0.0925')
			},
			'NASHVILLE': {
				'MEALS': Decimal('0.0925'),
				'SALES': Decimal('0.0925')
			}
		},
		'TX': {
			'HOUSTON': {
				'MEALS': Decimal('0.0825'),
				'SALES': Decimal('0.0825')
			},
			'SAN ANTONIO': {
				'MEALS': Decimal('0.0813'),
				'SALES': Decimal('0.0825')
			},
			'DALLAS': {
				'MEALS': Decimal('0.0825'),
				'SALES': Decimal('0.0825')
			},
			'AUSTIN': {
				'MEALS': Decimal('0.0825'),
				'SALES': Decimal('0.0825')
			},
			'FORT WORTH': {
				'MEALS': Decimal('0.0825'),
				'SALES': Decimal('0.0825')
			},
			'EL PASO': {
				'MEALS': Decimal('0.0825'),
				'SALES': Decimal('0.0825')
			},
			'ARLINGTON': {
				'MEALS': Decimal('0.08'),
				'SALES': Decimal('0.08')
			}
		},
		'VA': {
			'VIRGINIA BEACH': {
				'MEALS': Decimal('0.1050'),
				'SALES': Decimal('0.05')
			},
		},
		'WA': {
			'SEATTLE': {
				'MEALS': Decimal('0.10'),
				'SALES': Decimal('0.095')
			}
		},
		'WI': {
			'MILWAUKEE': {
				'MEALS': Decimal('0.0565'),
				'SALES': Decimal('0.056')
			}
		}
	},
	'NG': {
		'MEALS': Decimal('0.00'),
		'SALES': Decimal('0.05')
	},
	'GB': {
		'MEALS': Decimal('0.20'),
		'SALES': Decimal('0.18')
	}
}