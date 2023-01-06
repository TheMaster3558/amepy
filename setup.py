from setuptools import setup, find_packages
import re

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('pyame/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.rst') as f:
    readme = f.read()

setup(
    name='pyame',
    author='The Master',
    url='https://github.com/TheMaster3558/pyame',
    project_urls={
        'Documentation': 'https://pyame.readthedocs.io/en/latest/',
        'Github': 'https://github.com/TheMaster3558/pyame',
    },
    version=version,
    packages=find_packages(),
    license='MIT',
    description='A Python wrapper for the Discord API',
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.7.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)
