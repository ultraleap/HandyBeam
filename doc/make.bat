:: this version does not activate handybeam
@cls

:: htmldir works OK, but it is only suitable for an actual http server
:: @sphinx-build -b dirhtml -j 12 -E source build_htmldir

:: htmlhelp works kinda. The Ms HTMLHelp system is broken itself - it throws errors on browsing.
:: @sphinx-build -b htmlhelp -j 12 -E source build_htmlhelp

:: this is the most successfull version so far.
@sphinx-build -b html -j 12 -E source build_html


:: trialling this one just now
:: @sphinx-build -b epub -j 12 -E source build_epub

:: singlehtml file works OK -- but it actually does produce more than one file.
:: @sphinx-build -b singlehtml -j 12 -E source build_singlehtml

