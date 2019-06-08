"""
file :code:`bugcatcher.py` -- error reporting tool

Should an error or exception occur, it will be automatically submitted to BugSnag with stack trace.
This will help me to debug the problem quicker.

.. Note:: At this time, this facility it is completely disabled, but could be enabled in some circumstances.

"""

enable_bugsnag = True
""" flag: set to True to enable error reporting using bugsnag."""

enable_hostname_reporting = True
""" flag: if true, host name and login name will be included in the report."""


enable_auto_install = False
""" flag: set to True to enable automatic bugsnag installation on the target system."""

if enable_bugsnag:  # disable error reporting for development

    import logging
    import os
    import platform
    import socket
    import warnings
    import inspect

    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # print('starting bugcatcher at {}'.format(current_dir))

    def install_and_import(package):
        """
        install and import package
        this will attempt to import the specified package.
        If the package is not installed on the system, it will attempt to install it using pip,
        If it cannot be installed, and then imported, it fails.

        Example:
            install_and_import('bugsnag')
            install_and_import('pyopencl')

        :param package: what package to install/import.
        :return:
        """

        import importlib
        try:
            #  print('importing')
            importlib.import_module(package)
            #  print('import succeeded');
        except ImportError:
            if enable_auto_install:
                print('could not import "{}" -- attempting to install...'.format(package))
                os.system('pip install bugsnag')
                os.system('pip install cmocean')
                os.system('conda install -c conda-forge pyopencl')
            else:
                pass
        finally:
            # print('refreshing site')
            import site
            importlib.import_module('site')
            try:
                importlib.reload(site)
            # pylint: disable=W0702
            except ImportError:
                pass
            finally:
                # print('importing...')
                globals()[package] = importlib.import_module(package)
                # print('done.')


    # install and import essential dependencies
    # install_and_import('bugsnag')  # Note, this creates many problems
    import bugsnag

    # install_and_import('pyopencl')  # Note, this creates many problems
    # install_and_import('cmocean')  # Note, this creates many problems
    # install_and_import('pycuda')  # Note, this creates many problems

    # notify bugsnag that i am imported
    try:
        from bugsnag.handlers import BugsnagHandler
    except ImportError as e:
        print('No pip on the platform??? You must have pip. Contact Jurek for support on this.')
        raise RuntimeError("can't import a critical module. Contact Jurek for support.")

    # Now, start off the logger, and link the bugsnag to the logger.
    # From now, anything with "error" or higher, will also get submitted (asynchronously) to BugSnag.

    # pylint: disable = E0602
    # attempt to load the version ID from "previous_commit_hash.txt"

    git_commit = 'None'
    try:
        git_commit = open('{}\\previous_commit_hash.txt'.format(current_dir)).read(-1)
    except IOError:
        warnings.warn('no previous_commit_hash.txt file  at {} - trying git'.format(current_dir))
        # attempt to get version from current git
        try:
            import subprocess
            result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE)
            git_commit = result.stdout.decode('utf-8')
        except Exception as e:
            git_commit = 'unknown>1.2.0'
            warnings.warn('can''t ascertain my version using git')
            warnings.warn('exception type: {}, arguments: {}, string: {}'.format(type(e), e.args, e))

    # attempt to load version tag
    git_tag = 'None'
    try:
        git_tag = open('{}\\tag.txt'.format(current_dir)).read(-1)
    except IOError:
        try:
            warnings.warn('no tag.txt file at {} - trying git'.format(current_dir))
            # attempt to get it straight from git
            import subprocess

            result = subprocess.run(['git', 'describe'], stdout=subprocess.PIPE)
            git_tag = result.stdout.decode("utf-8")
        except Exception as e:
            git_tag = 'unknown tag >1.2.0'
            warnings.warn('can''t ascertain my version tag using git')
            warnings.warn('exception type: {}, arguments: {}, string: {}'.format(type(e), e.args, e))
  
    bugsnag.configure(
        api_key="e8f8e38698ff222ae1a9060aa443b75e",
        # Note: This is Jurek's private BugSnag account.
        # We might need to upgrade it later.
        project_root=current_dir,
        app_version=git_tag,
        ignore_classes=["django.http.Http404"],
        release_stage="development",
        # ! Note, asynchronous=False might be needed for this to work from inside Matlab. Enable otherwise to improve load performance.
        asynchronous=True)

    logger = logging.getLogger("basic")
    logger.setLevel(logging.INFO)
    logger.addHandler(BugsnagHandler())

    login = None
    hostname = None
    node = None
    if enable_hostname_reporting:
        login = os.getlogin()
        hostname = socket.gethostname()
        node = platform.node()

    bugsnag.notify(
        Exception("I have been imported"),
        context="bugcatcher.start",
        meta_data={
            "startup_data": {
                "login": login,
                "hostname": hostname,
                "node": node,
                "git_commit": git_commit,
                "git_tag": git_tag
            }
        }
    )
    # pylint: enable = E0602

    # raise ValueError('trying to catch something from Matlab')
    # zepta = 3/0
    # print("this is the end - should not be executed {}".format(zepta))
