===========================
Data collection and privacy
===========================

By default, HandyBeam uses `bugsnag.com <https://https://www.bugsnag.com/>`_ to spot crashes and errors. The exact code that does it is contained in the :py:mod:`handybeam.bugcatcher`.

You can inspect that module source code, and disable it by setting :py:attr:`handybeam.bugcatcher.enable_bugsnag` to :code:`False`.

Please do not do that tough. The code is configured to capture and report fatal crashes only. This will help me to debug HandyBeam.

The data is stored as per :code:`bugsnag` policy, for up to 7 days. ( I am on a free plan )

Upon exception, the following data is captured:

* stack trace: file names of the python source code and line numbers where the exception occurred. This might include the fully qualified path of the file on Your computer. Note that sometimes people put some personal data there like their name or project name.
* version tag, which is loaded from :code:`handybeam\tag.txt` file
* git commit hash if available, from :code:`handybeam\previous_commit_hash.txt` file
* if the version or git hash is not found in the text files, an attempt is made to ask the local git installation for the same data. This will only work if You have handybeam installed inside a git repository.

You might be marginally annoyed that I am also asking the code to provide:

* host name as reported by system's :code:`hostname` command
* log-in name, if available

If that's a problem, you can disable this part of the code by setting :py:attr:`handybeam.bugcatcher.enable_hostname_reporting` to :code:`False`

The record metadata also includes the exact time when the exception occurred.

No other data is recorded or stored.

The collected data is occasionally browsed to spot for typical exceptions, crashes e.t.c. No other analytics is performed.

I hope that's OK with You.

Jurek


.. include:: footer_licence_note.rst



