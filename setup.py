from setuptools import setup, find_packages
import os.path

def getversion(fname):
    """Get the __version__ reading the file: works both in Python 2.X and 3.X,
    whereas direct importing would break in Python 3.X with a syntax error"""
    for line in open(fname):
        if line.startswith('__version__'):
            return eval(line[13:])
    raise NameError('Missing __version__ in graphapi.py')

VERSION = getversion(
    os.path.join(os.path.dirname(__file__), 'src/strippers/mixi/graphapi.py'))


setup(
    name                 = 'strippers.mixi',
    version              = VERSION,
    author               = 'Tomohiro Otsuka',
    author_email         = 't.otsuka@gmail.com',
    description          = 'Python library for mixi Graph API',
    long_description     = open('README.rst').read(),
    url                  = 'http://pypi.python.org/pypi/strippers.mixi',
    license              = 'LGPL',
    keywords             = 'mixi oauth',
    install_requires     = ['setuptools', 'MultipartPostHandler'],
    package_dir          = {'strippers': 'src/strippers'},
    packages             = find_packages('src'),
    namespace_packages   = ['strippers'],
    include_package_data = True,
    zip_safe             = False,
    classifiers          = [
                            'Development Status :: 5 - Production/Stable',
                            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                            'Intended Audience :: Developers',
                            'Topic :: Software Development :: Libraries :: Python Modules',
                            'Operating System :: OS Independent',
                            'Natural Language :: Japanese',
                            ],
    )

