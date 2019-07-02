# mof_tda

Code for topological data analysis (TDA) on metal-organic frameworks (MOFs).

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