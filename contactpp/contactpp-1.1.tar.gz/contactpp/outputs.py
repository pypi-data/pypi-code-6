
import sys

def print_troullier_for_casino(pseudopotential,stream=sys.stdout):
    print_casino_polynomial_interaction(
            pseudopotential.coefficients,
            pseudopotential.cutoff,
            stream)

def print_utp_for_casino(pseudopotential,stream=sys.stdout):
    cutoff = pseudopotential.cutoff
    print_casino_polynomial_interaction(
            [ coeff / cutoff**icoeff for icoeff, coeff in 
                enumerate(pseudopotential.coefficients) ],
            cutoff,stream)

def print_casino_polynomial_interaction(coeffs,cutoff,stream=sys.stdout):
    stream.write("%block manual_interaction\n")
    stream.write("polynomial\n")
    stream.write("order : {}\n".format(len(coeffs)-1))
    stream.write("cutoff : {}\n".format(cutoff))
    for icoeff, coeff in enumerate(coeffs):
        stream.write("c_{} : {}\n".format(icoeff,coeff))
    stream.write("%endblock manual_interaction\n")

def print_swell_for_casino(pseudopotential,stream=sys.stdout):
    stream.write("%block manual_interaction\n")
    stream.write("square_well\n")
    stream.write("width : {}\n".format(pseudopotential.radius))
    stream.write("height : {}\n".format(pseudopotential.height))
    stream.write("%endblock manual_interaction\n")
