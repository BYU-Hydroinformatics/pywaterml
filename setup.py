from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='https://github.com/romer8/pywaterml.git',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="The pywaterml is a package that lets you handle WaterML functions such as GetValues, GetSitesInfo, etc. In addition it lets offers extra functions such as mean interpolation for data with gaps",
    license="MIT",
    author="Elkin Giovanni Romero Bustamante",
    author_email='gio.rombus@gmail.com',
    url='https://github.com/romer8/https://github.com/romer8/pywaterml.git',
    packages=['pywaterml'],
    entry_points={
        'console_scripts': [
            'pywaterml=pywaterml.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='https://github.com/romer8/pywaterml.git',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
