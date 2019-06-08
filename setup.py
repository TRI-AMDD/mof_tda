from setuptools import setup, find_packages


# TODO: add proper dependency versions
setup(name="mof_tda",
      packages=find_packages(),
      install_requires=["numpy",
                        "scipy",
                        "cmake",
                        "cgal",
                        "diode",
			"dionysus",
                        "persim",
                        "ripser",
                        "matplotlib"]
	)

