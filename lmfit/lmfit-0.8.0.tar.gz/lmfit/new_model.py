"""
Concise nonlinear curve fitting.
"""

import warnings
import inspect
import copy
import numpy as np
from . import Parameters, Minimizer
from .printfuncs import fit_report

# Use pandas.isnull for aligning missing data is pandas is available.
# otherwise use numpy.isnan
try:
    from pandas import isnull, Series
except ImportError:
    isnull = np.isnan
    Series = type(NotImplemented)

def _align(var, mask, data):
    "align missing data, with pandas is available"
    if isinstance(data, Series) and isinstance(var, Series):
        return var.reindex_like(data).dropna()
    elif mask is not None:
        return var[mask]
    return var

class Model(object):
    """Create a model from a user-defined function.

    Parameters
    ----------
    func: function to be wrapped
    independent_vars: list of strings or None (default)
        arguments to func that are independent variables
    param_names: list of strings or None (default)
        names of arguments to func that are to be made into parameters
    missing: None, 'none', 'drop', or 'raise'
        'none' or None: Do not check for null or missing values (default)
        'drop': Drop null or missing observations in data.
            if pandas is installed, pandas.isnull is used, otherwise
            numpy.isnan is used.
        'raise': Raise a (more helpful) exception when data contains null
            or missing values.
    name: None or string
        name for the model. When `None` (default) the name is the same as
        the model function (`func`).

    Note
    ----
    Parameter names are inferred from the function arguments,
    and a residual function is automatically constructed.

    Example
    -------
    >>> def decay(t, tau, N):
    ...     return N*np.exp(-t/tau)
    ...
    >>> my_model = Model(decay, independent_vars=['t'])
    """

    _forbidden_args = ('data', 'weights', 'params')
    _invalid_ivar  = "Invalid independent variable name ('%s') for function %s"
    _invalid_par   = "Invalid parameter name ('%s') for function %s"
    _invalid_missing = "missing must be None, 'none', 'drop', or 'raise'."
    _names_collide = "Two models have parameters named %s. Use distinct names"

    def __init__(self, func, independent_vars=None, param_names=None,
                 missing='none', prefix='', name=None, **kws):
        self.func = func
        self.prefix = prefix
        self.param_names = param_names
        self.independent_vars = independent_vars
        self.func_allargs = []
        self.func_haskeywords = False
        self._others = []
        if not missing in [None, 'none', 'drop', 'raise']:
            raise ValueError(self._invalid_missing)
        self.missing = missing
        self.opts = kws
        self.result = None
        self._parse_params()
        if self.independent_vars is None:
            self.independent_vars = []
        if name is None and hasattr(self.func, '__name__'):
            name = self.func.__name__
        self.name = name

    def _reprstring(self):
        out  = self.name
        if len(self.prefix) > 0:
            out = "%s(prefix='%s')" % (self.name, self.prefix)
        return out

    def __repr__(self):
        out  = self._reprstring()
        for other in self._others:
            out = "%s %s %s" % (out, other[1], other[0]._reprstring())
        return  "<lmfit.Model: %s>" % (out)

    def _parse_params(self):
        "build params from function arguments"
        if self.func is None:
            return
        argspec = inspect.getargspec(self.func)
        pos_args = argspec.args[:]
        keywords = argspec.keywords
        kw_args = {}
        if argspec.defaults is not None:
            for val in reversed(argspec.defaults):
                kw_args[pos_args.pop()] = val
        #
        self.func_haskeywords = keywords is not None
        self.func_allargs = pos_args + list(kw_args.keys())
        allargs = self.func_allargs

        if len(allargs) == 0 and keywords is not None:
            return

        # default independent_var = 1st argument
        if self.independent_vars is None:
            self.independent_vars = [pos_args[0]]

        # default param names: all positional args
        # except independent variables
        self.def_vals = {}
        if self.param_names is None:
            self.param_names = pos_args[:]
            for key, val in kw_args.items():
                if (not isinstance(val, bool) and
                    isinstance(val, (float, int))):
                    self.param_names.append(key)
                    self.def_vals[key] = val
            for p in self.independent_vars:
                if p in self.param_names:
                    self.param_names.remove(p)

        # check variables names for validity
        # The implicit magic in fit() requires us to disallow some
        fname = self.func.__name__
        for arg in self.independent_vars:
            if arg not in allargs or arg in self._forbidden_args:
                raise ValueError(self._invalid_ivar % (arg, fname))
        for arg in self.param_names:
            if arg not in allargs or arg in self._forbidden_args:
                raise ValueError(self._invalid_par % (arg, fname))

        names = []
        if self.prefix is None:
            self.prefix = ''
        for pname in self.param_names:
            names.append("%s%s" % (self.prefix, pname))
        self.param_names = set(names)

    def make_params(self, **kwargs):
        pars = Parameters()
        for name in self.param_names:
            pars.add(name)
            basename = name
            if self.prefix is not None:
                basename = name[len(self.prefix):]
            if basename in self.def_vals:
                pars[name].value = self.def_vals[basename]
            if basename in kwargs:
                pars[name].value = kwargs[basename]
        for other in self._others:
            pars.update(other[0].make_params(**kwargs))
        return pars

    def guess(self, data=None, **kws):
        """stub for guess starting values --
        should be implemented for each model subclass to
        run self.make_params(), update starting values
        and return a Parameters object"""
        cname = self.__class__.__name__
        msg = 'guess() not implemented for %s' % cname
        raise NotImplementedError(msg)

    def _residual(self, params, data, weights, **kwargs):
        "default residual:  (data-model)*weights"
        diff = self.eval(params, **kwargs) - data
        if weights is not None:
            diff *= weights
        return np.asarray(diff)  # for compatibility with pandas.Series

    def make_funcargs(self, params, kwargs):
        """convert parameter values and keywords to function arguments"""
        out = {}
        out.update(self.opts)
        npref = len(self.prefix)
        for name, par in params.items():
            if npref > 0 and name.startswith(self.prefix):
                name = name[npref:]
            if name in self.func_allargs or self.func_haskeywords:
                out[name] = par.value
        for name, val in kwargs.items():
            if name in self.func_allargs or self.func_haskeywords:
                out[name] = val
                if name in params:
                    params[name].value = val
        return out

    def _handle_missing(self, data):
        "handle missing data"
        if self.missing == 'raise':
            if np.any(isnull(data)):
                raise ValueError("Data contains a null value.")
        elif self.missing == 'drop':
            mask = ~isnull(data)
            if np.all(mask):
                return None  # short-circuit this -- no missing values
            mask = np.asarray(mask)  # for compatibility with pandas.Series
            return mask

    def _check_param_name_collisions(self, other):
        colliding_param_names = self.param_names & other.param_names
        if len(colliding_param_names) != 0:
            collision = colliding_param_names.pop()
            raise NameError(_names_collide % collision)

    def __add__(self, other):
        self._check_param_name_collisions(other)
        self._others.append( (other, '+') )
        return self

    def __sub__(self, other):
        self._check_param_name_collisions(other)
        self._others.append( (other, '-') )
        return self

    def __mul__(self, other):
        self._check_param_name_collisions(other)
        self._others.append( (other, '*') )
        return self

    def __div__(self, other):
        self._check_param_name_collisions(other)
        self._others.append( (other, '/') )
        return self

    def eval(self, params, **kwargs):
        """evaluate the model with the supplied parameters"""
        fcnargs = self.make_funcargs(params, kwargs)
        result = self.func(**fcnargs)
        for mod, op in self._others:
            other = mod.eval(params, **kwargs)
            if   op == '+': result += other
            elif op == '-': result -= other
            elif op == '*': result *= other
            elif op == '/': result /= other
        return result

    def fit(self, data, params, weights=None, method='leastsq',
            iter_cb=None, scale_covar=True, **kwargs):
        """Fit the model to the data.

        Parameters
        ----------
        data: array-like
        params: Parameters object
        weights: array-like of same size as data
            used for weighted fit
        method: fitting method to use (default = 'leastsq')
        iter_cb:  None or callable  callback function to call at each iteration.
        scale_covar:  bool (default True) whether to auto-scale covariance matrix
        keyword arguments: optional, named like the arguments of the
            model function, will override params. See examples below.

        Returns
        -------
        lmfit.Minimizer

        Examples
        --------
        # Take t to be the independent variable and data to be the
        # curve we will fit.

        # Using keyword arguments to set initial guesses
        >>> result = my_model.fit(data, tau=5, N=3, t=t)

        # Or, for more control, pass a Parameters object.
        >>> result = my_model.fit(data, params, t=t)

        # Keyword arguments override Parameters.
        >>> result = my_model.fit(data, params, tau=5, t=t)

        Note
        ----
        All parameters, however passed, are copied on input, so the original
        Parameter objects are unchanged.

        """
        params = copy.deepcopy(params)

        # If any kwargs match parameter names, override params.
        param_kwargs = set(kwargs.keys()) & self.param_names
        for name in param_kwargs:
            p = kwargs[name]
            if isinstance(p, Parameter):
                p.name = name  # allows N=Parameter(value=5) with implicit name
                params[name] = copy.deepcopy(p)
            else:
                params[name].set(value=p)
            del kwargs[name]

        # All remaining kwargs should correspond to independent variables.
        for name in kwargs.keys():
            if not name in self.independent_vars:
                warnings.warn("The keyword argument %s does not" % name +
                              "match any arguments of the model function." +
                              "It will be ignored.", UserWarning)

        # If any parameter is not initialized raise a more helpful error.
        missing_param = any([p not in params.keys()
                             for p in self.param_names])
        blank_param = any([(p.value is None and p.expr is None)
                           for p in params.values()])
        if missing_param or blank_param:
            raise ValueError("""Assign each parameter an initial value by
 passing Parameters or keyword arguments to fit""")

        # Handle null/missing values.
        mask = None
        if self.missing not in (None, 'none'):
            mask = self._handle_missing(data)  # This can raise.
            if mask is not None:
                data = data[mask]
            if weights is not None:
                weights = _align(weights, mask, data)

        # If independent_vars and data are alignable (pandas), align them,
        # and apply the mask from above if there is one.
        for var in self.independent_vars:
            if not np.isscalar(self.independent_vars):  # just in case
                kwargs[var] = _align(kwargs[var], mask, data)

        output = ModelFitResult(self, params, method=method, iter_cb=iter_cb,
                                scale_covar=scale_covar, fcn_kws=kwargs)
        output.fit(data=data, weight=weights)
        return output

class ModelFitResult(Minimizer):
    def __init__(self, model, params, data=None, weights=None,
                 method='leastsq', fcn_args=None, fcn_kws=None,
                 iter_cb=None, scale_covar=True, **fit_kws):
        self.model = model
        super(ModelFitResult, self).__init__(model._residual, params,
                                             fcn_args=fcn_args,
                                             fcn_kws=fcn_kws,
                                             iter_cb=iter_cb,
                                             scale_covar=scale_covar,
                                             **fit_kws)
        self.data = data
        self.weights = weights
        self.method = method
        self.init_params = copy.deepcopy(params)

    def fit(self, data=None, params=None, weights=None, method=None, **kwargs):

        if data is not None:
            self.data = data
        if params is not None:
            self.params = params
        if weights is not None:
            self.weights = weights
        if method is not None:
            self.method = method
        self.userargs = (self.data, self.weights)
        self.userkws.update(kwargs)
        self.init_params = copy.deepcopy(self.params)
        self.init_values = self.model.make_funcargs(self.init_params, {})
        self.init_fit    = self.model.eval(params=self.init_params, **self.userkws)

        self.minimize(method=self.method)
        self.best_fit = self.model.eval(params=self.params, **self.userkws)

    def eval(self, **kwargs):
        self.userkws.update(kwargs)
        return self.model.eval(params=self.params, **self.userkws)

    def fit_report(self, modelpars=None, show_correl=True, min_correl=0.1):
        "return fit report"
        report =fit_report(self, modelpars=modelpars,
                           show_correl=show_correl,
                           min_correl=min_correl)
        out = '[[Model]]\n    %s\n%s' % (repr(self.model), report)
        return out
