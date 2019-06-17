from setuptools import setup, find_packages


# TODO: specify dependency
setup(name="mof_tda",
      packages=find_packages(),
      setup_requires=["Cython",
                      "numpy",
                      ],
      install_requires=["scipy",
                        "diode",
                        "dionysus",
                        "persim",
                        "ripser",
                        "matplotlib",
                        ],
      dependency_links=['git+ssh://git@github.com/mrzv/diode#egg=diode']
      )
