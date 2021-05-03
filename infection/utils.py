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
        d[k] = v
