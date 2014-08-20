###########################################################################
#                                                                         #
# pyhobdcalc: an multibase calculator python module written in C.         #
# Copyright (C) 2014 Bruggemann Eddie.                                    #
#                                                                         #
# This file is part of pyhobdcalc python module.                          #
# pyhobdcalc is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# pyhobdcalc is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the            #
# GNU General Public License for more details.                            # 
#                                                                         # 
# You should have received a copy of the GNU General Public License       #
# along with pyhobdcalc. If not, see <http://www.gnu.org/licenses/>       #
#                                                                         # 
###########################################################################

from distutils.core import Extension, setup

with open("README/README.rst",'r') as file :
  long_description = file.read()

MODULE_NAME="pyhobdcalc"

setup(name=MODULE_NAME,version='1.0.0',
      url='https://github.com/mrcyberfighter/pyhobdcalc',
      author="Eddie Bruggemann",author_email="mrcyberfighter@gmail.com",
      maintainer="Eddie Bruggemann",maintainer_email="mrcyberfighter@gmail.com",
      long_description=long_description,
      description="pyhobdcalc is an multibase (bases: 2,8,10,16) conversion and calculating python module written in C. With signed integers and floats converting, adding, substract, multiplying and dividing functions.",
      packages=['pyhodbcalc'],
      package_dir={'pyhodbcalc': '.'},
      package_data={'pyhodbcalc':["Documentation/*.zip",
				  "License/*.txt",
				  "README/*.rst",
				  
				  "hobdcalc/hobdcalc_assertions.c",
				  "hobdcalc/hobdcalc.c",
				  "hobdcalc/conversion/int_bin/int_bin.c",
				  "hobdcalc/conversion/int_oct/int_oct.c",
				  "hobdcalc/conversion/int_hex/int_hex.c",
				  "hobdcalc/conversion/float_to_bin/float_bin.c",
				  "hobdcalc/conversion/float_to_oct/float_oct.c",
				  "hobdcalc/conversion/float_to_hex/float_hex.c",
				  "hobdcalc/conversion/utils/conversion_utils.c",
			      
				  "hobdcalc/operations/int_result/calc_bin_int_operations.c",
				  "hobdcalc/operations/int_result/calc_oct_int_operations.c",
				  "hobdcalc/operations/int_result/calc_hex_int_operations.c",
				  "hobdcalc/operations/float_result/calc_bin_float_operations.c",
				  "hobdcalc/operations/float_result/calc_oct_float_operations.c",
				  "hobdcalc/operations/float_result/calc_hex_float_operations.c",
			           
			          "pyhobdcalc/utils/string_utils.c", 
				  "pyhobdcalc/conversion/bin_func.c",
				  "pyhobdcalc/conversion/oct_func.c",
				  "pyhobdcalc/conversion/hex_func.c",
				  "pyhobdcalc/operations/integer/bin_func.c",
				  "pyhobdcalc/operations/integer/oct_func.c",
				  "pyhobdcalc/operations/integer/hex_func.c",
				  "pyhobdcalc/operations/float/bin_func.c",
				  "pyhobdcalc/operations/float/oct_func.c",
				  "pyhobdcalc/operations/float/hex_func.c",]},
      
      platforms=["Linux"],license="GPLv3",
      ext_modules=[Extension(MODULE_NAME,["pyhobdcalc.c",])] )