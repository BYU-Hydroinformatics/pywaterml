from setuptools import setup
import versioneer

# with open("README.md", "r") as readme:
#     long_description = readme.read()
#
# with open('requirements.txt', 'r') as req:
#     requirements = req.read().splitlines()

requirements = [
    "xmltodict",
    "pandas",
    "numpy",
    "owslib",
    "suds-community",
    "scikit-learn==0.22",
    "tslearn",
]

setup(
    name='pywaterml',
    # version='0.0.14.dev1',
    # version='1.1.1',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="The pywaterml is a package that lets you handle WaterML functions such as GetValues, GetSitesInfo, etc. In addition it lets offers extra functions such as mean interpolation for data with gaps",
    license='BSD 3-Clause',
    license_family='BSD',
    author="Elkin Giovanni Romero Bustamante",
    author_email='gio.rombus@gmail.com',
    url='https://github.com/BYU-Hydroinformatics/pywaterml',
    packages=['pywaterml'],
    install_requires=requirements,
    keywords='WaterML',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Hydrology',
        'Topic :: Scientific/Engineering :: Visualization',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
    ]
)
