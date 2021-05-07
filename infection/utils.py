"""
-------------------------------------------------------
Utils for infection package
-------------------------------------------------------
Author:  Mark Fruman
Email:   majorgowan@yahoo.com
-------------------------------------------------------
"""
import string
import numpy as np


def supdate(d, update, specials=None):
    """
    Apply an update to a dictionary with special handling for
    specified sub-dictionaries.

    Operators:
        "+key": <new_value(s)>
            Top-level (including within "special" subdicts) list-valued
            parameters may be extended by specifying an update with
            {"+key": [<new_value(s)>]} instead of {"key": [<new value(s)>]}
            which will still clobber the existing value.

    Parameters
    ----------
    d : dict
        dictionary to be updated
    update : dict
        the update to apply
    specials : list
        special keys; keys in specials that appear in update should be
        used to update the subdictionaries in d instead of clobbering them
    """
    if specials is None:
        specials = ["infection", "mobility"]

    for k, v in update.items():
        if k in specials and d[k] is not None:
            supdate(d[k], v, specials=[])
        elif k.startswith("+"):
            kk = k[1:]
            if not isinstance(v, list):
                v = [v]
            if d.get(kk, None) is None:
                d[kk] = v
            elif not isinstance(d[kk], list):
                d[kk] = [d[kk]] + v
            else:
                d[kk].extend(v)
        else:
            d[k] = v


def random_choice(values_obj, size=None, positive=True):
    """
    Replace values_obj with a single value as follows:
        - if values_obj is a list, select one element with uniform probability
        - if values_obj is a dict with keys "dist" (str) and "params",
          generate a value using the numpy.random function "dist" with
          parameters "params"; e.g. for a non-uniform random choice:
            {"dist": "choice",
             "params": {"a": [choice_1, choice_2, choice_3],
                        "p": [0.3, 0.5, 0.2]}}
        - otherwise return values_obj unchanged

    Parameters
    ----------
    values_obj : list or dict or object
        value to be parsed
    size : int
        if specified, return a list of value
    positive : bool
        if set, return absolute value of result (numpy distribution only)

    Returns
    -------
    number or object or list
    """
    if isinstance(values_obj, list):
        return np.random.choice(values_obj, size=size)
    if isinstance(values_obj, dict) and "dist" in values_obj:
        params = {**values_obj.get("params"), **{"size": size}}
        result = getattr(np.random,
                         values_obj["dist"])(**params)
        if positive:
            return np.abs(result)
        else:
            return result
    if size is not None:
        return size * [values_obj]
    return values_obj


def random_string(length=8):
    """
    Generate a random string of digits and letters.

    Parameters
    ----------
    length : int

    Returns
    -------
    str
    """
    return "".join(np.random.choice(list(string.ascii_letters)
                                    + list(string.digits), length))
