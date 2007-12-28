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
"""Support for Layout Templates

$Id$
"""
__docformat__ = "reStructuredText"

import zope.component
from z3c.template.interfaces import ILayoutTemplate


class FormLayoutSupport(object):
    """Layout support for forms except IAddForm."""

    layout = None

    def __call__(self):
        self.update()
        if self.layout is None:
            layout = zope.component.getMultiAdapter((self, self.request),
                ILayoutTemplate)
            return layout(self)
        return self.layout()


class AddFormLayoutSupport(object):
    """Layout support for IAddForm."""

    layout = None

    def __call__(self):
        self.update()
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ''
        if self.layout is None:
            layout = zope.component.getMultiAdapter((self, self.request),
                ILayoutTemplate)
            return layout(self)
        return self.layout()
