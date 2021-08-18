#!/usr/bin/env python
from setuptools import setup

setup(name='goldencheetah scripts',
      description='GoldenCheetah python scripts',
      version='0.1',
      classifiers=['Development Status :: 4 - Beta',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   ],
      long_description=open('README.md').read(),
      url='',
      author_email='lbusoni@gmail.com',
      author='Lorenzo Busoni',
      license='',
      keywords='bike, power, cycling',
      packages=['gc_scripts',
                ],
      install_requires=["numpy",
                        ],
      package_data={
          'gc_scripts': ['data/*'],
      },
      include_package_data=True,
      test_suite='test',
      )
