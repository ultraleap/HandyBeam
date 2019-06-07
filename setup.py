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
        packages = ['handybeam',
                    'handybeam.cl',
                    'handybeam.cl_py_ref_code',
                    'handybeam.opencl_wrappers',
                    'handybeam.propagator_mixins',
                    'handybeam.samplers',
                    'handybeam.solver_mixins',
                    'handybeam.test_code',
                    'handybeam.tests',
                    'handybeam.translator_mixins'],
        install_requires = [
                'markdown',
                'numpy',
                'pybind11',
                'mako',
                'pyparsing',
                'cycler',
                'pyopencl',
                'cmocean',
                'matplotlib=2.1',
                'opencv-python',
                'pyquaternion',
                'jupyter',
                'pyopengl',
                'PyQt5',
                'vispy',
        ],
        test_suite = 'nose.collector',
        tests_require = ['nose', 'nose-cover3'],
        include_package_data = True,
        zip_safe = False
)
