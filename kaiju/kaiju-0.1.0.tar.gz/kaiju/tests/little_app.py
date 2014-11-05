import random

import kaiju
from kaiju.arguments import Data, Float, Int, RawString, Bool

trilotest_database_name = "trilotest"

trilotest = kaiju.Kaiju(trilotest_database_name)
trilotest.connect_database()


@trilotest(output="bigdata")
def generate_uniform(a, b, sample_size, seed=1138):
    random.seed(seed)
    for _ in xrange(sample_size):
        yield random.randint(a, b)


@trilotest(sample=Data("bigdata"), output="bigdata")
def squared(sample):
    for x in sample:
        yield x * x


@trilotest(sample=Data("bigdata"))
def mean(sample):
    def sum_vec(x, y):
        return x[0] + y[0], x[1] + y[1]
    mean_data_gen = ((x, 1) for x in sample)
    sample_sum, sample_count = reduce(sum_vec, mean_data_gen, (0.0, 0.0))
    yield sample_sum / sample_count


@trilotest(my_int=Int(), my_float=Float(), my_string=RawString(), my_bool=Bool())
def some_arguments_testing(my_int, my_float, my_string="string", my_bool=False):
    yield dict(my_bool=my_bool, my_int=my_int, my_float=my_float, my_string=my_string)


@trilotest(pokemons=Data("pokemon"))
def provide_pokemons(pokemons):
    return pokemons
