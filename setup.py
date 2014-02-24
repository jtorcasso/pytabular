from setuptools import setup

setup(
    name='PyTabular',
    version='0.1.3',
    author='Jake C. Torcasso',
    author_email='jaketorcasso@gmail.com',
    packages=['pytabular'],
    scripts=['bin/PyTabular_tutorial.ipynb'],
    url='http://pypi.python.org/pypi/PyTabular/',
    license='LICENSE.txt',
    description='Package for creating LateX tables.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.8.0",
    ],
)
