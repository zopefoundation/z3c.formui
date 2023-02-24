##############################################################################
#
# Copyright (c) 2005-2009 Zope Foundation and Contributors.
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
"""Test Setup
"""
import doctest
import unittest

import z3c.form.outputchecker
import z3c.form.testing


def setUpZPT(test):
    z3c.form.testing.setUpZPT(test)
    from z3c.macro.tales import MacroExpression
    from zope.browserpage.metaconfigure import registerType
    from zope.contentprovider.tales import TALESProviderExpression
    registerType('macro', MacroExpression)
    registerType('provider', TALESProviderExpression)


# def setUpZ3CPT(test):
#     z3c.form.testing.setUpZ3CPT(test)
#     from z3c.macro.tales import z3cpt_macro_expression
#     from zope.component import provideUtility
#     provideUtility(z3cpt_macro_expression, name='macro')


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            'README.txt',
            setUp=setUp,
            tearDown=z3c.form.testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            checker=z3c.form.testing.outputChecker)
        # for setUp in (setUpZPT, setUpZ3CPT)]) # XXX: broken macro tests
        for setUp in (setUpZPT, )])
