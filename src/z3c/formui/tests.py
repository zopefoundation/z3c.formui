##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
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
"""
$Id: tests.py 72087 2007-01-18 01:03:33Z rogerineichen $
"""
__docformat__ = "reStructuredText"

import unittest
from zope.testing import doctest

from z3c.form import testing

def setUpZPT(test):
    testing.setUpZPT(test)
    from zope.app.pagetemplate.metaconfigure import registerType
    from zope.contentprovider.tales import TALESProviderExpression
    from z3c.macro.tales import MacroExpression
    registerType('macro', MacroExpression)
    registerType('provider', TALESProviderExpression)

def setUpZ3CPT(test):
    testing.setUpZ3CPT(test)
    from zope.component import provideUtility
    from z3c.macro.tales import z3cpt_macro_expression
    provideUtility(z3cpt_macro_expression, name='macro')

def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=testing.OutputChecker(doctest))
        #for setUp in (setUpZPT, setUpZ3CPT)]) # XXX: broken macro tests
        for setUp in (setUpZPT, )])
