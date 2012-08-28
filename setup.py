##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup

$Id$
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='z3c.formui',
    version='2.3.1dev',
    author="Stephan Richter, Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="A set of initial UI components for z3c.form.",
    long_description=(
        read('README.txt')
        + '\n\n' +
        '.. contents::'
        + '\n\n' +
        read('src', 'z3c', 'formui', 'README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license="ZPL 2.1",
    keywords="zope3 form widget",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url='http://pypi.python.org/pypi/z3c.formui',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require=dict(
        test=['z3c.form [test]',
              'z3c.form [latest]'],
        ),
    install_requires=[
        'setuptools',
        'z3c.form >= 2.2.0',
        'z3c.macro',
        'z3c.template',
        'zope.component',
        'zope.publisher',
        'zope.viewlet',
        ],
    zip_safe=False,
    )
