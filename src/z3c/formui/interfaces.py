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
"""Form UI Interfaces

$Id$
"""
__docformat__ = "reStructuredText"
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewletManager

class IFormUILayer(IBrowserRequest):
    """A basic layer for the Form UI package."""

class IDivFormLayer(IFormUILayer):
    """A layer that supports forms created only using DIV elements."""

class ITableFormLayer(IFormUILayer):
    """A layer that supports forms created using tables."""

class ICSS(IViewletManager):
    """CSS viewlet manager."""
