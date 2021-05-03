"""
-------------------------------------------------------
Utils for infection package
-------------------------------------------------------
Author:  Mark Fruman
Email:   majorgowan@yahoo.com
-------------------------------------------------------
"""


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
