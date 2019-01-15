# Copyright (C) 2018 SaltStack
import ast
import re
from setuptools import setup
import sys
import versioneer

assert sys.version_info >= (3, 6, 0), 'saltstack-black requires Python 3.6+'
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    readme_md = CURRENT_DIR / 'README.md'
    with open(readme_md, encoding='utf8') as ld_file:
        return ld_file.read()


setup(
    name='SQ-Black',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='The uncompromising, single quotes, code formatter.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    keywords='automation formatter yapf autopep8 pyfmt gofmt rustfmt black',
    author='Pedro Algarvio',
    author_email='pedro@algarvio.me',
    url='https://github.com/s0undt3ch/sq-black',
    license='Apache Software License 2.0',
    packages=['sqblack'],
    python_requires='>=3.6',
    zip_safe=False,
    install_requires=['black>=18.9b0'],
    test_suite='tests.test_sqblack',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    entry_points={'console_scripts': ['sq-black=sqblack.cli:main']},
)
