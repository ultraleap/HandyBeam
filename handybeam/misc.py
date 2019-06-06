"""
file :code:`misc.py`, module :py:mod:`handybeam.misc`

Functions and helpers that would not fit anywhere else.

Some of them might be awaiting refactoring or deletion.

"""


def copy_docstring(from_function, separator="\n", prepend=True):


    '''
    -----------------------------------------------
    copy_docstring(from_function,separator,prepend)
    -----------------------------------------------
            
    DESCRIPTION HERE

    Parameters
    ----------

    from_function : DESCRIPTION HERE
            DESCRIPTION HERE
    separator : DESCRIPTION HERE
            DESCRIPTION HERE
    prepend : DESCRIPTION HERE
            DESCRIPTION HERE
    
    '''



    """
    Decorator. Copies the docstring of `from_function` into the decorated function.

    This is used to make the documentation of the overriding methods nicer: enables to join the documentation of the super class and the current class in a single place.

    if :code:`prepend` is true, the current(local) function's goes first. Otherwise, the :code:`from_function`'s docstring goes first.

    Modified and extended from `https://stackoverflow.com/questions/13741998 <https://stackoverflow.com/questions/13741998/is-there-a-way-to-let-classes-inherit-the-documentation-of-their-superclass-with>`_
    """


    def _decorator(func):
        '''
        ---------------------------------------------
        _decorator(func)
        ---------------------------------------------
                
        DESCRIPTION HERE

        Parameters
        ----------

        func : DESCRIPTION HERE
                DESCRIPTION HERE
        
        '''

        
        """ creates a new, modified function, to be returned instead of the original.

        Combines the docstrings of two functions: the decorated, and the one from  'from_function'
        """
        
        source_doc = from_function.__doc__

        if func.__doc__ is None:  # if there is no docstring at the local function
            func.__doc__ = source_doc
        else:  # if there is, connect the two
            if prepend:
                func.__doc__ = separator.join([func.__doc__, source_doc])
            else:
                func.__doc__ = separator.join([source_doc, func.__doc__, ])

        return func
    return _decorator


class HandyDict(dict):
    """

    Provides matlab-like setting/storage of items in a dict

    q=HandyDict()
    q.new_key = 'Hello world!'
    print(q.new_key)



    happily copypasted from https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """
    def __init__(self, args={'True': True, 'False':False}):
        super(HandyDict, self).__init__(args)
        if isinstance(args, dict):
            for k, v in args.items():
                if not isinstance(v, dict):
                    self[k] = v
                else:
                    self.__setattr__(k, HandyDict(v))

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(HandyDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(HandyDict, self).__delitem__(key)
        del self.__dict__[key]
