from setuptools import setup, find_packages


setup(name="mof_tda",
      packages=find_packages(),
      # TODO: figure out cython/ripser install
      # TODO: add diode install
      install_requires=["numpy",
                        # "Cython",
                        "scipy",
                        "pymatgen",
                        "cmake",
                        "ase",
                        # "cgal",
                        "diode",
                        "dionysus",
                        "persim",
                        # "ripser",
                        "matplotlib"],
      )
