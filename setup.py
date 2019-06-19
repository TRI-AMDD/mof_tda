from setuptools import setup, find_packages


# TODO: specify dependency
setup(name="mof_tda",
      packages=find_packages(),
      setup_requires=["Cython",
                      "numpy==1.15",
                      ],
      install_requires=["scipy",
                        "diode",
                        "dionysus",
                        "persim",
                        "ripser",
                        "matplotlib",
                        "pymatgen",
                        "ase",
                        ],
      dependency_links=['http://github.com/mrzv/diode/tarball/master#egg=diode']
      )
