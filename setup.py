from setuptools import setup

setup(
    name='ONEG',
    version='0.1.0b1',
    install_requires=['numpy'],
    extras_require={
        'tests': ['pytest'],
        'develop': ['restructuredtext-lint>=1.1.3',
                    'sphinx-rtd-theme>=0.4.1'
                    'sphinx>=1.8.1',
                    'sphinx-autobuild>=0.7.1',
                    'recommonmark>=0.4.0',
                    'm2r>=0.2']
    },
    license='MIT License'
)