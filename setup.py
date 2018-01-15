
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()
setup(
    name='difm',
    version='1.0.0',
    license='GNU',
    description='https://github.com/fmnet/difm',
    long_description=readme,
    author='fmnet',
    author_email='',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'difm=difm.cli:DIFM'
        ]
    }
)