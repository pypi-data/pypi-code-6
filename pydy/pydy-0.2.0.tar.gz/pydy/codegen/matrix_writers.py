class MatrixWriter():

    def _generate_sub_expressions(self, int_var='z_'):

        names = []
        expressions = []
        for name, matrix in self.matrix_dict.items():
            names.append(name)
            for entry in matrix:
                expressions.append(entry)

        self.sub_expressions, expressions = cse(expressions,
                                                numbered_symbols(int_var))

        matrices = {}
        index = 0
        for name in names:
            num_rows, num_cols = self.matrix_dict[name].shape
            matrices[name] = Matrix(expressions[index:index + num_rows *
                                     num_columns]).reshape(num_rows,
                                                           num_columns)
            index += num_rows * num_cols



    def _pick_alternate_cse_symbol(self):

        symbols = {}
        for name, matrix in self.matrix_dict.items():
            symbols += matrix.atoms(Symbol)
            symbols += matrix.atoms(Function)

    # need to somehow get the function names, like 'sin'
    # In [156]: res[0].atoms(sm.Function)
    # Out[156]: {sin(q1(t)), sin(q2(t)), q1(t), q2(t), cos(q1(t) - q2(t))}


        list_of_lists = self.symbols.values()
        if None in list_of_lists:
            list_of_lists.remove(None)
        all_symbols = list(chain.from_iterable(list_of_lists))
        while Symbols(int_var) in all_symbols:
            int_var = random.choice(all_letters) + '_'

    def print(self, matrix_dict, cse=False, cse_symbol='z_'):
