date /T > git_response.txt.tmp
git rm -r --cached .
git add .
git commit -m "$1"
