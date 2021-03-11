# mof_tda

Code for topological data analysis (TDA) on metal-organic frameworks (MOFs).
This software and assets were used to perform the analysis detailed in the work
published [here](https://arxiv.org/abs/2010.00532).  This code is no longer actively 
maintained, but an extended software with similar and extended functionality 
can be found in the [molecule-tda](https://github.com/a1k12/molecule-tda) repo.


## Installation

### OSX
Install CGAL and CMake via homebrew.
```angular2
brew install cgal cmake
```

Install via setup.py

```angular2
python setup.py develop
```

### Linux

Install CGAL/CMake through apt and then setup.py develop

```angular2
$ apt-get install cgal cmake gcc g++
$ export CXX=/usr/bin/g++
$ export CC=/usr/bin/gcc
$ python setup.py develop
```