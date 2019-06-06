'''
Reference: https://python-packaging.readthedocs.io/en/latest/everything.html
'''

from setuptools import setup 

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
        name = 'handybeam',
        version = '1.0',
        long_description = readme(),
        classifiers=[
                'Development Status :: ',
                'License :: ',
                'Programming Languages :: Python :: , OpenCL :: ',
                'Topics :: ',
        ],
        keywords = '',
        url = '',
        authors = [

        ],
        author_email = '',
        license = '',
        packages = ['handybeam'],
        install_requires = [
                'markdown',
                'numpy',
                'pybind11',
                'pyparsing',
                'cycler',
                'pyopencl',
                'cmocean',
                'matplotlib',
                'vispy',
                'opencv-python',
                'pyquaternion',
                'jupyter',
                'mako',

        ],
        test_suite = 'nose.collector',
        tests_require = ['nose', 'nose-cover3'],
        include_package_data = True,
        zip_safe = False
)
