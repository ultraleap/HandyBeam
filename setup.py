""" Prepare an installable pip package out of handybeam source code


Reference: https://python-packaging.readthedocs.io/en/latest/everything.html

"""

from setuptools import setup 


def readme():  # type: () -> str
    with open('README.rst') as f:
        return f.read()

setup(
        name='handybeam',
        version='1.0',
        long_description=readme(),
        classifiers=[
                'Development Status :: ',
                'License :: ',
                'Programming Languages :: Python :: , OpenCL :: ',
                'Topics :: ',
        ],
        keywords='',
        url='',
        authors=['Jerzy Dziewierz', 'Ultrahaptics', 'Salvador Catsis'],
        author_email='JerzyDziewierz-UH@ultrahaptics.com',
        license='Apache v2.0',
        packages=['handybeam',
                    'handybeam.cl',
                    'handybeam.cl_py_ref_code',
                    'handybeam.opencl_wrappers',
                    'handybeam.propagator_mixins',
                    'handybeam.samplers',
                    'handybeam.solver_mixins',
                    'handybeam.test_code',
                    'handybeam.tests',
                    'handybeam.translator_mixins'],
        install_requires=[
                'markdown==3.1.1',
                'numpy==1.16.4',
                'pybind11==2.2.4',
                'mako==1.0.12',
                'pyparsing==2.4.0',
                'cycler==0.10.0',
                'pyopencl==2018.2.5',
                'cmocean==2.0',
                'matplotlib==3.1.0',
                'opencv-python==4.2.0.32',
                'pyquaternion==0.9.5',
                'jupyter==1.0.0',
                'PyOpenGL==3.1.0',
                'PyQt5==5.12.2',
                'vispy==0.5.3',
                'Mako',
                'Pybind11',
        ],
        test_suite='nose.collector',
        tests_require=['nose', 'nose-cover3'],
        include_package_data=True,
        zip_safe=False
)
