import mock
import random
import shlex
import unittest
from bson.objectid import ObjectId

from kaiju.cli import KaijuCLI

from . import little_app


class KaijuTests(unittest.TestCase):

    def setUp(self):
        self.cli = KaijuCLI(little_app.trilotest.operations,
                            description="Little test app")
        little_app.trilotest.drop_database()

    def tearDown(self):
        little_app.trilotest.reset_flags()
        little_app.trilotest.drop_database()

    def test_generation(self):
        s_a, s_b = -5, 6
        s_size = 20
        s_seed = 1138
        a = little_app.generate_uniform(s_a, s_b, sample_size=s_size,
                                        seed=s_seed)

        random.seed(s_seed)
        reference_data = [random.randint(s_a, s_b) for _ in xrange(s_size)]
        self.assertIsInstance(a, ObjectId)

        recorded_data = little_app.trilotest.fetch(a, collection="bigdata")
        self.assertItemsEqual(recorded_data, reference_data)

    def test_run_sequence(self):
        a = little_app.generate_uniform(-5, 5, 100, seed=1138)
        b = little_app.squared(sample=a)

        stored_log = little_app.trilotest.fetch_log(a)
        stored_log.pop("date")
        self.assertEqual(
            stored_log,
            {
                "_id": a,
                "operation": "generate_uniform",
                "kwargs": {"a": -5, "b": 5, "sample_size": 100, "seed": 1138},
                "output": "bigdata",
            }
        )

        stored_log = little_app.trilotest.fetch_log(b)
        stored_log.pop("date")
        self.assertEqual(
            stored_log,
            {
                u"_id": b,
                u"operation": u"squared",
                u"kwargs": {u"sample": a},
                u"output": u"bigdata",
            }
        )

        self.assertAlmostEqual(little_app.mean(sample=a).next(), -0.31,
                               delta=1e-12)
        self.assertAlmostEqual(little_app.mean(sample=b).next(), 9.45,
                               delta=1e-12)

    def test_names(self):
        self.assertItemsEqual(
            little_app.trilotest.operations.keys(),
            ["generate_uniform", "squared", "mean", "some_arguments_testing",
             "provide_pokemons"]
        )

    def test_var(self):
        test_var_name = "__TRILOBITE_TEST_VARIABLE"

        self.assertIsNone(little_app.trilotest.var_get(test_var_name).next())

        # Set variable
        test_value_1 = 12321
        result_1 = little_app.trilotest.var_set(test_var_name,
                                                test_value_1).next()

        self.assertEqual(result_1["ok"], 1.0)
        self.assertEqual(result_1["n"], 1)
        self.assertFalse(result_1["updatedExisting"])
        self.assertIsInstance(result_1["upserted"], ObjectId)

        # Get variable value
        self.assertEqual(little_app.trilotest.var_get(test_var_name).next(),
                         test_value_1)

        # Update value
        test_value_2 = 65456
        result_2 = little_app.trilotest.var_set(test_var_name,
                                                test_value_2).next()

        self.assertEqual(result_2["ok"], 1.0)
        self.assertEqual(result_2["n"], 1)
        self.assertTrue(result_2["updatedExisting"])

        # List variables
        self.assertEqual(little_app.trilotest.var_get(test_var_name).next(),
                         test_value_2)

        result_ls = little_app.trilotest.var_ls().next()
        self.assertEqual(result_ls["name"], test_var_name)
        self.assertEqual(result_ls["value"], test_value_2)

        # Delete variable
        result_del = little_app.trilotest.var_del(test_var_name).next()
        result_del["ok"] == 1.0
        result_del["n"] == 1

        # Check if it was really deleted
        self.assertEqual(list(little_app.trilotest.var_ls()), [])

    def _execute_shell(self, shell_cmd):
        gargs, args = self.cli.parse_args(shlex.split(shell_cmd))
        little_app.trilotest.handle_kaiju_arguments(gargs)
        operation = gargs["operation"]
        return little_app.trilotest.execute(operation, args)

    def test_simple_usage_and_defaults(self):
        [output] = list(self._execute_shell("some_arguments_testing 1 0.2"))
        self.assertEqual(output, dict(my_bool=False, my_int=1, my_float=0.2,
                                      my_string="string"))

    def test_bool_store_true(self):
        [output] = list(self._execute_shell(
            "some_arguments_testing 1 0.2 --my_bool"
        ))
        self.assertEqual(output, dict(my_bool=True, my_int=1, my_float=0.2,
                                      my_string="string"))

    def test_arguments_default_parse(self):
        [output] = list(self._execute_shell(
            "some_arguments_testing 1 0.2 --my_string str"
        ))
        self.assertEqual(output, dict(my_bool=False, my_int=1, my_float=0.2,
                                      my_string="str"))

    @mock.patch("sys.stderr", mock.Mock())
    def test_type_check_int_can_be_float(self):
        with self.assertRaises(SystemExit):
            self._execute_shell("some_arguments_testing 0.1 2")

    @mock.patch("sys.stderr", mock.Mock())
    def test_type_check_int_cant_be_str(self):
        with self.assertRaises(SystemExit):
            self._execute_shell("some_arguments_testing abc 2")

    @mock.patch("sys.stderr", mock.Mock())
    def test_type_check_float_cant_be_str(self):
        with self.assertRaises(SystemExit):
            self._execute_shell("some_arguments_testing 1 abc")

    @mock.patch("sys.stderr", mock.Mock())
    def test_mandatory_arguments_are_mandatory(self):
        with self.assertRaises(SystemExit):
            self._execute_shell("some_arguments_testing")

    def test_data_argument_parse(self):
        oid1 = ObjectId("a" * 24)
        oid2 = ObjectId("b" * 24)
        little_app.trilotest.database.pokemon.insert([
            {"maker_id": oid1, "value": {"type": "fire", "name": "Charizard"}},
            {"maker_id": oid1, "value": {
                "type": "water", "name": "Blastoise"}},
            {"maker_id": oid1, "value": {"type": "grass", "name": "Venusaur"}},
            {"maker_id": oid2, "value": {
                "type": "fire", "name": "Typhlosion"}},
            {"maker_id": oid2, "value": {"type": "water", "name": "Feraligatr"}},
            {"maker_id": oid2, "value": {"type": "grass", "name": "Meganium"}},
        ])

        cmd = r"provide_pokemons {}".format("a" * 24)
        pokemons = list(self._execute_shell(cmd))

        self.assertItemsEqual(
            pokemons,
            [
                {"type": "fire", "name": "Charizard"},
                {"type": "water", "name": "Blastoise"},
                {"type": "grass", "name": "Venusaur"},
            ]
        )

    def test_memoized_results_arent_recalculated(self):
        cmd = "generate_uniform 0 10 10"
        first_run = self._execute_shell(cmd)
        second_run = self._execute_shell(cmd)

        self.assertEqual(first_run, second_run)

    def test_no_memo_forces_execution(self):
        cmd = "generate_uniform 0 10 10"
        cmd_no_memo = "--no-memo generate_uniform 0 10 10"

        results = []
        results.append(self._execute_shell(cmd))
        results.append(self._execute_shell(cmd))
        results.append(self._execute_shell(cmd_no_memo))

        self.assertEqual(results[0], results[1])
        self.assertNotEqual(results[1], results[2])

    def test_no_store_flag(self):
        cmd = "generate_uniform 0 10 10 --seed 1138"
        result1 = self._execute_shell(cmd)
        cmd = "--no-store generate_uniform 0 10 10 --seed 1138"
        result2 = self._execute_shell(cmd)

        self.assertEqual(type(result1), ObjectId)
        self.assertEqual(
            list(result2),
            [3, 5, 3, 1, 7, 4, 3, 8, 4, 1]
        )
