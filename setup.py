import setuptools
 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='inventory_optimisation_gd', 
    packages=['inventory_optimisation_gd'], 
    version='0.0.1',
    license='MIT',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=[
        'Marko Nikolic', 
        'Dejan Dzunja', 
        'Andrei Novikov'
        ],
    author_email=[
        'mnikolic@griddynamics.com', 
        'ddzunja@griddynamics.com', 
        'annovikov@griddynamics.com'
        ],
    url='https://github.com/griddynamics/rnd-inventory-optimization-dataiku',
    install_requires=[         
        'numpy',
        'ortools',
        'pandas',
        'numpy',
        'PyYAML',
    ],
    keywords=["optimization", "inventory", "startkit"],
)