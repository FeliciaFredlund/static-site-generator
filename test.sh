# -m tells which module to use
# discover -s is pointing at the directory to find the tests
# -v makes the output more verbose: showing all the test method names and the result for each
python -m unittest discover -s src -v