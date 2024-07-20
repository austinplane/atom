from setuptools import setup
setup(
        name='atom',
        version='0.1.0',
        packages=['atom'],
        entry_points=
        {
            'console_scripts': ['atom = atom.main:app']
        }
     )
