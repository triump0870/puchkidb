# Uninstall the packages install by setup.py
python setup.py install --record files.txt

# This will cause all the installed files to be printed to that directory.
# Then when you want to uninstall it simply run; be careful with the 'sudo'

cat files.txt | xargs rm -rf