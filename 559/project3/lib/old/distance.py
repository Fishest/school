"""
Function Reference
------------------

Distance functions between two vectors ``u`` and ``v``. Computing
distances over a large collection of vectors is inefficient for these
functions. Use ``pdist`` for this purpose.

+------------------+-------------------------------------------------+
|*Function*        | *Description*                                   |
+------------------+-------------------------------------------------+
| braycurtis       | the Bray-Curtis distance.                       |
+------------------+-------------------------------------------------+
| canberra         | the Canberra distance.                          |
+------------------+-------------------------------------------------+
| chebyshev        | the Chebyshev distance.                         |
+------------------+-------------------------------------------------+
| cityblock        | the Manhattan distance.                         |
+------------------+-------------------------------------------------+
| correlation      | the Correlation distance.                       |
+------------------+-------------------------------------------------+
| cosine           | the Cosine distance.                            |
+------------------+-------------------------------------------------+
| dice             | the Dice dissimilarity (boolean).               |
+------------------+-------------------------------------------------+
| euclidean        | the Euclidean distance.                         |
+------------------+-------------------------------------------------+
| hamming          | the Hamming distance (boolean).                 |
+------------------+-------------------------------------------------+
| jaccard          | the Jaccard distance (boolean).                 |
+------------------+-------------------------------------------------+
| kulsinski        | the Kulsinski distance (boolean).               |
+------------------+-------------------------------------------------+
| mahalanobis      | the Mahalanobis distance.                       |
+------------------+-------------------------------------------------+
| matching         | the matching dissimilarity (boolean).           |
+------------------+-------------------------------------------------+
| minkowski        | the Minkowski distance.                         |
+------------------+-------------------------------------------------+
| rogerstanimoto   | the Rogers-Tanimoto dissimilarity (boolean).    |
+------------------+-------------------------------------------------+
| russellrao       | the Russell-Rao dissimilarity (boolean).        |
+------------------+-------------------------------------------------+
| seuclidean       | the normalized Euclidean distance.              |
+------------------+-------------------------------------------------+
| sokalmichener    | the Sokal-Michener dissimilarity (boolean).     |
+------------------+-------------------------------------------------+
| sokalsneath      | the Sokal-Sneath dissimilarity (boolean).       |
+------------------+-------------------------------------------------+
| sqeuclidean      | the squared Euclidean distance.                 |
+------------------+-------------------------------------------------+
| yule             | the Yule dissimilarity (boolean).               |
+------------------+-------------------------------------------------+

References
----------

.. [Sta07] "Statistics toolbox." API Reference Documentation. The MathWorks.
   http://www.mathworks.com/access/helpdesk/help/toolbox/stats/.
   Accessed October 1, 2007.

.. [Mti07] "Hierarchical clustering." API Reference Documentation.
   The Wolfram Research, Inc.
   http://reference.wolfram.com/mathematica/HierarchicalClustering/tutorial/HierarchicalClustering.html.
   Accessed October 1, 2007.

.. [Gow69] Gower, JC and Ross, GJS. "Minimum Spanning Trees and Single Linkage
   Cluster Analysis." Applied Statistics. 18(1): pp. 54--64. 1969.

.. [War63] Ward Jr, JH. "Hierarchical grouping to optimize an objective
   function." Journal of the American Statistical Association. 58(301):
   pp. 236--44. 1963.

.. [Joh66] Johnson, SC. "Hierarchical clustering schemes." Psychometrika.
   32(2): pp. 241--54. 1966.

.. [Sne62] Sneath, PH and Sokal, RR. "Numerical taxonomy." Nature. 193: pp.
   855--60. 1962.

.. [Bat95] Batagelj, V. "Comparing resemblance measures." Journal of
   Classification. 12: pp. 73--90. 1995.

.. [Sok58] Sokal, RR and Michener, CD. "A statistical method for evaluating
   systematic relationships." Scientific Bulletins. 38(22):
   pp. 1409--38. 1958.

.. [Ede79] Edelbrock, C. "Mixture model tests of hierarchical clustering
   algorithms: the problem of classifying everybody." Multivariate
   Behavioral Research. 14: pp. 367--84. 1979.

.. [Jai88] Jain, A., and Dubes, R., "Algorithms for Clustering Data."
   Prentice-Hall. Englewood Cliffs, NJ. 1988.

.. [Fis36] Fisher, RA "The use of multiple measurements in taxonomic
   problems." Annals of Eugenics, 7(2): 179-188. 1936


Copyright Notice
----------------

Copyright (C) Damian Eads, 2007-2008. New BSD License.

"""
import sys, inspect
import numpy as np
import types
from predicates import *

# --------------------------------------------------------------------------- # 
# Distance Functions
# --------------------------------------------------------------------------- # 

def minkowski(u, v, p):
    r"""
    Computes the Minkowski distance between two vectors ``u`` and ``v``,
    defined as

    .. math::

       {||u-v||}_p = (\sum{|u_i - v_i|^p})^{1/p}.

    :Parameters:
       u : ndarray
           An n-dimensional vector.
       v : ndarray
           An n-dimensional vector.
       p : ndarray
           The norm of the difference :math:`{||u-v||}_p`.

    :Returns:
       d : double
           The Minkowski distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    if p < 1:
        raise ValueError("p must be at least 1")
    return (abs(u-v)**p).sum() ** (1.0 / p)

def wminkowski(u, v, p, w):
    r"""
    Computes the weighted Minkowski distance between two vectors ``u``
    and ``v``, defined as

    .. math::

       \left(\sum{(w_i |u_i - v_i|^p)}\right)^{1/p}.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.
       p : ndarray
           The norm of the difference :math:`{||u-v||}_p`.
       w : ndarray
           The weight vector.

    :Returns:
       d : double
           The Minkowski distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    if p < 1:
        raise ValueError("p must be at least 1")
    return ((w * abs(u-v))**p).sum() ** (1.0 / p)

def euclidean(u, v):
    """
    Computes the Euclidean distance between two n-vectors ``u`` and ``v``,
    which is defined as

    .. math::

       {||u-v||}_2

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Euclidean distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    q=np.matrix(u-v)
    return np.sqrt((q*q.T).sum())

def sqeuclidean(u, v):
    """
    Computes the squared Euclidean distance between two n-vectors u and v,
    which is defined as

    .. math::

       {||u-v||}_2^2.


    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The squared Euclidean distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return ((u-v)*(u-v).T).sum()

def cosine(u, v):
    r"""
    Computes the Cosine distance between two n-vectors u and v, which
    is defined as

    .. math::

       \frac{1-uv^T}
            {||u||_2 ||v||_2}.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Cosine distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return (1.0 - (np.dot(u, v.T) / \
                   (np.sqrt(np.dot(u, u.T)) * np.sqrt(np.dot(v, v.T)))))

def correlation(u, v):
    r"""
    Computes the correlation distance between two n-vectors ``u`` and
    ``v``, which is defined as

    .. math::

       \frac{1 - (u - \bar{u}){(v - \bar{v})}^T}
            {{||(u - \bar{u})||}_2 {||(v - \bar{v})||}_2^T}

    where :math:`\bar{u}` is the mean of a vectors elements and ``n``
    is the common dimensionality of ``u`` and ``v``.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The correlation distance between vectors ``u`` and ``v``.
    """
    umu = u.mean()
    vmu = v.mean()
    um = u - umu
    vm = v - vmu
    return 1.0 - (np.dot(um, vm) /
                  (np.sqrt(np.dot(um, um)) \
                   * np.sqrt(np.dot(vm, vm))))

def hamming(u, v):
    r"""
    Computes the Hamming distance between two n-vectors ``u`` and
    ``v``, which is simply the proportion of disagreeing components in
    ``u`` and ``v``. If ``u`` and ``v`` are boolean vectors, the Hamming
    distance is

    .. math::

       \frac{c_{01} + c_{10}}{n}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Hamming distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return (u != v).mean()

def jaccard(u, v):
    r"""
    Computes the Jaccard-Needham dissimilarity between two boolean
    n-vectors u and v, which is

    .. math::

         \frac{c_{TF} + c_{FT}}
              {c_{TT} + c_{FT} + c_{TF}}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Jaccard distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return (np.double(np.bitwise_and((u != v),
                     np.bitwise_or(u != 0, v != 0)).sum())
            /  np.double(np.bitwise_or(u != 0, v != 0).sum()))

def kulsinski(u, v):
    r"""
    Computes the Kulsinski dissimilarity between two boolean n-vectors
    u and v, which is defined as

    .. math::

         \frac{c_{TF} + c_{FT} - c_{TT} + n}
              {c_{FT} + c_{TF} + n}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Kulsinski distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    n = len(u)
    (nff, nft, ntf, ntt) = nbool_correspond_all(u, v)

    return (ntf + nft - ntt + n) / (ntf + nft + n)

def seuclidean(u, v, V):
    """
    Returns the standardized Euclidean distance between two n-vectors
    ``u`` and ``v``. ``V`` is an m-dimensional vector of component
    variances. It is usually computed among a larger collection
    vectors.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The standardized Euclidean distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    V = np.asarray(V, order='c')
    if len(V.shape) != 1 or V.shape[0] != u.shape[0] or u.shape[0] != v.shape[0]:
        raise TypeError('V must be a 1-D array of the same dimension as u and v.')
    return np.sqrt(((u-v)**2 / V).sum())

def cityblock(u, v):
    r"""
    Computes the Manhattan distance between two n-vectors u and v,
    which is defined as

    .. math::

       \sum_i {(u_i-v_i)}.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The City Block distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return abs(u-v).sum()

def mahalanobis(u, v, VI):
    r"""
    Computes the Mahalanobis distance between two n-vectors ``u`` and ``v``,
    which is defiend as

    .. math::

       (u-v)V^{-1}(u-v)^T

    where ``VI`` is the inverse covariance matrix :math:`V^{-1}`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Mahalanobis distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    VI = np.asarray(VI, order='c')
    return np.sqrt(np.dot(np.dot((u-v),VI),(u-v).T).sum())

def chebyshev(u, v):
    r"""
    Computes the Chebyshev distance between two n-vectors u and v,
    which is defined as

    .. math::

       \max_i {|u_i-v_i|}.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Chebyshev distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return max(abs(u-v))

def braycurtis(u, v):
    r"""
    Computes the Bray-Curtis distance between two n-vectors ``u`` and
    ``v``, which is defined as

    .. math::

       \sum{|u_i-v_i|} / \sum{|u_i+v_i|}.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Bray-Curtis distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return abs(u-v).sum() / abs(u+v).sum()

def canberra(u, v):
    r"""
    Computes the Canberra distance between two n-vectors u and v,
    which is defined as

    .. math::

       \frac{\sum_i {|u_i-v_i|}}
            {\sum_i {|u_i|+|v_i|}}.


    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Canberra distance between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    return abs(u-v).sum() / (abs(u).sum() + abs(v).sum())

def yule(u, v):
    r"""
    Computes the Yule dissimilarity between two boolean n-vectors u and v,
    which is defined as


    .. math::

         \frac{R}{c_{TT} + c_{FF} + \frac{R}{2}}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n` and :math:`R = 2.0 * (c_{TF} + c_{FT})`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Yule dissimilarity between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    (nff, nft, ntf, ntt) = nbool_correspond_all(u, v)
    return float(2.0 * ntf * nft) / float(ntt * nff + ntf * nft)

def matching(u, v):
    r"""
    Computes the Matching dissimilarity between two boolean n-vectors
    u and v, which is defined as

    .. math::

       \frac{c_{TF} + c_{FT}}{n}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Matching dissimilarity between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    (nft, ntf) = nbool_correspond_ft_tf(u, v)
    return float(nft + ntf) / float(len(u))

def dice(u, v):
    r"""
    Computes the Dice dissimilarity between two boolean n-vectors
    ``u`` and ``v``, which is

    .. math::

         \frac{c_{TF} + c_{FT}}
              {2c_{TT} + c_{FT} + c_{TF}}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Dice dissimilarity between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    if u.dtype == np.bool:
        ntt = (u & v).sum()
    else:
        ntt = (u * v).sum()
    (nft, ntf) = nbool_correspond_ft_tf(u, v)
    return float(ntf + nft) / float(2.0 * ntt + ntf + nft)

def rogerstanimoto(u, v):
    r"""
    Computes the Rogers-Tanimoto dissimilarity between two boolean
    n-vectors ``u`` and ``v``, which is defined as

    .. math::
       \frac{R}
            {c_{TT} + c_{FF} + R}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n` and :math:`R = 2(c_{TF} + c_{FT})`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Rogers-Tanimoto dissimilarity between vectors
           ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    (nff, nft, ntf, ntt) = nbool_correspond_all(u, v)
    return float(2.0 * (ntf + nft)) / float(ntt + nff + (2.0 * (ntf + nft)))

def russellrao(u, v):
    r"""
    Computes the Russell-Rao dissimilarity between two boolean n-vectors
    ``u`` and ``v``, which is defined as

    .. math::

      \frac{n - c_{TT}}
           {n}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Russell-Rao dissimilarity between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    if u.dtype == np.bool:
        ntt = (u & v).sum()
    else:
        ntt = (u * v).sum()
    return float(len(u) - ntt) / float(len(u))

def sokalmichener(u, v):
    r"""
    Computes the Sokal-Michener dissimilarity between two boolean vectors
    ``u`` and ``v``, which is defined as

    .. math::

       \frac{2R}
            {S + 2R}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n`, :math:`R = 2 * (c_{TF} + c_{FT})` and
    :math:`S = c_{FF} + c_{TT}`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Sokal-Michener dissimilarity between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    if u.dtype == np.bool:
        ntt = (u & v).sum()
        nff = (~u & ~v).sum()
    else:
        ntt = (u * v).sum()
        nff = ((1.0 - u) * (1.0 - v)).sum()
    (nft, ntf) = nbool_correspond_ft_tf(u, v)
    return float(2.0 * (ntf + nft))/float(ntt + nff + 2.0 * (ntf + nft))

def sokalsneath(u, v):
    r"""
    Computes the Sokal-Sneath dissimilarity between two boolean vectors
    ``u`` and ``v``,

    .. math::

       \frac{2R}
            {c_{TT} + 2R}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\mathtt{u[k]} = i` and :math:`\mathtt{v[k]} = j` for
    :math:`k < n` and :math:`R = 2(c_{TF} + c_{FT})`.

    :Parameters:
       u : ndarray
           An :math:`n`-dimensional vector.
       v : ndarray
           An :math:`n`-dimensional vector.

    :Returns:
       d : double
           The Sokal-Sneath dissimilarity between vectors ``u`` and ``v``.
    """
    u = np.asarray(u, order='c')
    v = np.asarray(v, order='c')
    if u.dtype == np.bool:
        ntt = (u & v).sum()
    else:
        ntt = (u * v).sum()
    (nft, ntf) = nbool_correspond_ft_tf(u, v)
    return float(2.0 * (ntf + nft))/float(ntt + 2.0 * (ntf + nft))

# --------------------------------------------------------------------------- # 
# Distance Wrapper Method
# --------------------------------------------------------------------------- # 

__dist_methods = []
def __register():
    self = sys.modules[__name__]
    for name in dir(self):
        method = getattr(self, name)
        if inspect.isfunction(method) and not name.startswith('_'):
            __dist_methods.append((name, method))
__register()

def distance(u, v, method="euclidean"):
    ''' Helper method to abstract the distance method strategy

    :param u: The first vector to compute the distance
    :param v: The second vector to compute the distance
    :param method: The distance algorithm to use
    :returns: The result of the distance algorithm
    '''
    for name, func in __dist_methods:
        if method.lower() == name:
            return func(u,v)
    raise Exception("Sorting method %s does not exist" % method)
