"""
Function Reference
------------------

Predicates for checking the validity of distance matrices, both
condensed and redundant. Also contained in this module are functions
for computing the number of observations in a distance matrix.

+------------------+-------------------------------------------------+
|*Function*        | *Description*                                   |
+------------------+-------------------------------------------------+
|is_valid_dm       | checks for a valid distance matrix.             |
+------------------+-------------------------------------------------+
|is_valid_y        | checks for a valid condensed distance matrix.   |
+------------------+-------------------------------------------------+
|num_obs_dm        | # of observations in a distance matrix.         |
+------------------+-------------------------------------------------+
|num_obs_y         | # of observations in a condensed distance       |
|                  | matrix.                                         |
+------------------+-------------------------------------------------+

Copyright Notice
----------------

Copyright (C) Damian Eads, 2007-2008. New BSD License.

"""
import numpy as np
import types

# --------------------------------------------------------------------------- # 
# Helper Functions
# --------------------------------------------------------------------------- # 

def is_valid_dm(D, tol=0.0, throw=False, name="D", warning=False):
    """
    Returns True if the variable D passed is a valid distance matrix.
    Distance matrices must be 2-dimensional numpy arrays containing
    doubles. They must have a zero-diagonal, and they must be symmetric.

    :Parameters:
       D : ndarray
           The candidate object to test for validity.
       tol : double
           The distance matrix should be symmetric. tol is the maximum
           difference between the :math:`ij`th entry and the
           :math:`ji`th entry for the distance metric to be
           considered symmetric.
       throw : bool
           An exception is thrown if the distance matrix passed is not
           valid.
       name : string
           the name of the variable to checked. This is useful ifa
           throw is set to ``True`` so the offending variable can be
           identified in the exception message when an exception is
           thrown.
       warning : boolx
           Instead of throwing an exception, a warning message is
           raised.

    :Returns:
       Returns ``True`` if the variable ``D`` passed is a valid
       distance matrix.  Small numerical differences in ``D`` and
       ``D.T`` and non-zeroness of the diagonal are ignored if they are
       within the tolerance specified by ``tol``.
    """
    D = np.asarray(D, order='c')
    valid = True
    try:
        s = D.shape
        if D.dtype != np.double:
            if name:
                raise TypeError('Distance matrix \'%s\' must contain doubles (double).' % name)
            else:
                raise TypeError('Distance matrix must contain doubles (double).')
        if len(D.shape) != 2:
            if name:
                raise ValueError('Distance matrix \'%s\' must have shape=2 (i.e. be two-dimensional).' % name)
            else:
                raise ValueError('Distance matrix must have shape=2 (i.e. be two-dimensional).')
        if tol == 0.0:
            if not (D == D.T).all():
                if name:
                    raise ValueError('Distance matrix \'%s\' must be symmetric.' % name)
                else:
                    raise ValueError('Distance matrix must be symmetric.')
            if not (D[xrange(0, s[0]), xrange(0, s[0])] == 0).all():
                if name:
                    raise ValueError('Distance matrix \'%s\' diagonal must be zero.' % name)
                else:
                    raise ValueError('Distance matrix diagonal must be zero.')
        else:
            if not (D - D.T <= tol).all():
                if name:
                    raise ValueError('Distance matrix \'%s\' must be symmetric within tolerance %d.' % (name, tol))
                else:
                    raise ValueError('Distance matrix must be symmetric within tolerance %5.5f.' % tol)
            if not (D[xrange(0, s[0]), xrange(0, s[0])] <= tol).all():
                if name:
                    raise ValueError('Distance matrix \'%s\' diagonal must be close to zero within tolerance %5.5f.' % (name, tol))
                else:
                    raise ValueError('Distance matrix \'%s\' diagonal must be close to zero within tolerance %5.5f.' % tol)
    except Exception, e:
        if throw:
            raise
        if warning:
            _warning(str(e))
        valid = False
    return valid

def is_valid_y(y, warning=False, throw=False, name=None):
    """
    Returns ``True`` if the variable ``y`` passed is a valid condensed
    distance matrix. Condensed distance matrices must be 1-dimensional
    numpy arrays containing doubles. Their length must be a binomial
    coefficient :math:`{n \choose 2}` for some positive integer n.


    :Parameters:
       y : ndarray
           The condensed distance matrix.

       warning : bool
           Invokes a warning if the variable passed is not a valid
           condensed distance matrix. The warning message explains why
           the distance matrix is not valid.  'name' is used when
           referencing the offending variable.

       throws : throw
           Throws an exception if the variable passed is not a valid
           condensed distance matrix.

       name : bool
           Used when referencing the offending variable in the
           warning or exception message.

    """
    y = np.asarray(y, order='c')
    valid = True
    try:
        if type(y) != np.ndarray:
            if name:
                raise TypeError('\'%s\' passed as a condensed distance matrix is not a numpy array.' % name)
            else:
                raise TypeError('Variable is not a numpy array.')
        if y.dtype != np.double:
            if name:
                raise TypeError('Condensed distance matrix \'%s\' must contain doubles (double).' % name)
            else:
                raise TypeError('Condensed distance matrix must contain doubles (double).')
        if len(y.shape) != 1:
            if name:
                raise ValueError('Condensed distance matrix \'%s\' must have shape=1 (i.e. be one-dimensional).' % name)
            else:
                raise ValueError('Condensed distance matrix must have shape=1 (i.e. be one-dimensional).')
        n = y.shape[0]
        d = int(np.ceil(np.sqrt(n * 2)))
        if (d*(d-1)/2) != n:
            if name:
                raise ValueError('Length n of condensed distance matrix \'%s\' must be a binomial coefficient, i.e. there must be a k such that (k \choose 2)=n)!' % name)
            else:
                raise ValueError('Length n of condensed distance matrix must be a binomial coefficient, i.e. there must be a k such that (k \choose 2)=n)!')
    except Exception, e:
        if throw:
            raise
        if warning:
            _warning(str(e))
        valid = False
    return valid

def num_obs_dm(d):
    """
    Returns the number of original observations that correspond to a
    square, redudant distance matrix ``D``.

    :Parameters:
       d : ndarray
           The target distance matrix.

    :Returns:
       The number of observations in the redundant distance matrix.
    """
    d = np.asarray(d, order='c')
    _is_valid_dm(d, tol=np.inf, throw=True, name='d')
    return d.shape[0]

def num_obs_y(Y):
    """
    Returns the number of original observations that correspond to a
    condensed distance matrix ``Y``.

    :Parameters:
       Y : ndarray
           The number of original observations in the condensed
           observation ``Y``.

    :Returns:
       n : int
           The number of observations in the condensed distance matrix
           passed.
    """
    Y = np.asarray(Y, order='c')
    _is_valid_y(Y, throw=True, name='Y')
    k = Y.shape[0]
    if k == 0:
        raise ValueError("The number of observations cannot be determined on an empty distance matrix.")
    d = int(np.ceil(np.sqrt(k * 2)))
    if (d*(d-1)/2) != k:
        raise ValueError("Invalid condensed distance matrix passed. Must be some k where k=(n choose 2) for some n >= 2.")
    return d

def nbool_correspond_all(u, v):
    if u.dtype != v.dtype:
        raise TypeError("Arrays being compared must be of the same data type.")

    if u.dtype == np.int or u.dtype == np.float_ or u.dtype == np.double:
        not_u = 1.0 - u
        not_v = 1.0 - v
        nff = (not_u * not_v).sum()
        nft = (not_u * v).sum()
        ntf = (u * not_v).sum()
        ntt = (u * v).sum()
    elif u.dtype == np.bool:
        not_u = ~u
        not_v = ~v
        nff = (not_u & not_v).sum()
        nft = (not_u & v).sum()
        ntf = (u & not_v).sum()
        ntt = (u & v).sum()
    else:
        raise TypeError("Arrays being compared have unknown type.")

    return (nff, nft, ntf, ntt)

def nbool_correspond_ft_tf(u, v):
    if u.dtype == np.int or u.dtype == np.float_ or u.dtype == np.double:
        not_u = 1.0 - u
        not_v = 1.0 - v
        nff = (not_u * not_v).sum()
        nft = (not_u * v).sum()
        ntf = (u * not_v).sum()
        ntt = (u * v).sum()
    else:
        not_u = ~u
        not_v = ~v
        nft = (not_u & v).sum()
        ntf = (u & not_v).sum()
    return (nft, ntf)


def copy_array_if_base_present(a):
    """
    Copies the array if its base points to a parent array.
    """
    if a.base is not None:
        return a.copy()
    elif np.issubsctype(a, np.float32):
        return array(a, dtype=np.double)
    else: return a

def copy_arrays_if_base_present(T):
    """
    Accepts a tuple of arrays T. Copies the array T[i] if its base array
    points to an actual array. Otherwise, the reference is just copied.
    This is useful if the arrays are being passed to a C function that
    does not do proper striding.
    """
    return [copy_array_if_base_present(a) for a in T]

def convert_to_bool(X):
    if X.dtype != np.bool:
        X = np.bool_(X)
    if not X.flags.contiguous:
        X = X.copy()
    return X

def convert_to_double(X):
    if X.dtype != np.double:
        X = np.double(X)
    if not X.flags.contiguous:
        X = X.copy()
    return X

