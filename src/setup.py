import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='tuliptask',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    scripts=['bin/tulip'],
    license='MIT License',
    description='Simple task runner for applications set up with docker and kubernetes',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/pzmosquito/tuliptask',
    author='Peter Zhang',
    author_email='pzmosquito@gmail.com',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)