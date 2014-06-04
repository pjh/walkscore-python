walkscore-python
================

A Python3 wrapper around the [Walk Score APIs](http://www.walkscore.com/professional/developers.php). Initially this is just meant for playing around and getting familiar with the API, but with the later intention of mashing up walk scores with e.g. building permit or crime data from [data.seattle.gov](http://www.data.seattle.gov).

Before using the code in this repository, the following dependencies must be satisfied:
* The [pjh/pyutils](https://github.com/pjh/pyutils) repository must be checked out somewhere and a symlink to pyutils/pjh_utils.py must be created in the util subdirectory of this repository.

Run `./main.py -h` to see help and usage.

Todo list:
* Create additional classes under apis/ for transit score and travel time APIs. Perhaps inherit all of these classes from one common base class.

