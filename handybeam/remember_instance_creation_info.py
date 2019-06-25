# documentation: OK.
"""
file :code:`remember_instance_creation_info.py` -- tools helpful for debugging.

"""
import threading
import time
import traceback


class InstanceCreationError(Exception):
    """ Debug helper.

    Currently, just a pass - but could be used to do something (e.g. log an error) if needed.

    """
    pass


class RememberInstanceCreationInfo:
    """ Debug helper.

    Make Your objects inherit this class to receive the benefits.

    provides to a subclass:

    * :code:`self.creation_name`

    * :code:`self.creation_module`

    * :code:`self.creation_file`

    * :code:`self.creation_file`

    * :code:`self.creation_line`

    * :code:`self.creation_function`

    * :code:`self.creation_text`

    Sourced from `Stack overflow <https://stackoverflow.com/questions/1690400/getting-an-instance-name-inside-class-init/49331683#49331683>`_

    """

    def __init__(self):
        """
        constructor. Starts a thread to figure out the super's creation info and bails out.
        """
        try:
            # pylint: disable = W0612
            for frame, line in traceback.walk_stack(None):
                varnames = frame.f_code.co_varnames
                if varnames is ():
                    break
                if frame.f_locals[varnames[0]] not in (self, self.__class__):
                    break
                    # if the frame is inside a method of this instance,
                    # the first argument usually contains either the instance or
                    #  its class
                    # we want to find the first frame, where this is not the case
            else:
                pass  # note: this is notorious when used from matlab. Just skip.
                # raise InstancecreationError("No suitable outer frame found.")
            # pylint: disable = W0631
            self._outer_frame = frame
            self.creation_module = frame.f_globals["__name__"]
            self.creation_file, self.creation_line, self.creation_function, \
                self.creation_text = traceback.extract_stack(frame, 1)[0]
            self.creation_name = self.creation_text.split("=")[0].strip()
            super().__init__()
            threading.Thread(target=self._check_existence_after_creation).start()
        except Exception:
            pass

    def _check_existence_after_creation(self):
        """
        Helper function for :py:class:`RememberInstanceCreationInfo <handybeam.remember_instance_creation_info.RememberInstanceCreationInfo>`

        :return: raises an error if the object's data is not found
        """
        while self._outer_frame.f_lineno == self.creation_line:
            time.sleep(0.01)
        # this is executed as soon as the line number changes
        # now we can be sure the instance was actually created
        error = InstanceCreationError(
                "\ncreation name not found in creation frame.\ncreation_file: "
                "%s \ncreation_line: %s \ncreation_text: %s\ncreation_name ("
                "might be wrong): %s" % (
                    self.creation_file, self.creation_line, self.creation_text,
                    self.creation_name))
        nameparts = self.creation_name.split(".")
        try:
            var = self._outer_frame.f_locals[nameparts[0]]
        except KeyError:
            # raise error
            pass
        finally:
            del self._outer_frame
        # make sure we have no permanent inter frame reference
        # which could hinder garbage collection
        try:
            for name in nameparts[1:]: 
                var = getattr(var, name)
        except AttributeError:
            # raise error
            pass
        if var is not self:
            pass
            # raise error

    def __repr__(self):
        """ part of :code:`RememberInstanceCreationInfo`.
        Overrides the regular :code:`__repr__()`,
        and adds the creation name to the existing object's :code:`__repr__()`"""
        return super().__repr__()[
               :-1] + " with creation_name '%s'>" % self.creation_name
    
    def print_debug_creation_info(self):
        """ helper method of :py:class:`RememberInstanceCreationInfo <handybeam.remember_instance_creation_info.RememberInstanceCreationInfo>`

        :return: prints the debug data
        """
        print(self.creation_name, self.creation_module, self.creation_function,
              self.creation_line, self.creation_text, sep=", ")
