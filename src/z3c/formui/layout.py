##############################################################################
#
# Copyright (c) 2007-2009 Zope Foundation and Contributors.
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


REDIRECT_STATUS_CODES = (301, 302, 303)


class FormLayoutSupport(object):
    """Layout support for forms except IAddForm."""

    layout = None

    def __call__(self):
        self.update()

        if self.request.response.getStatus() in REDIRECT_STATUS_CODES:
            # don't bother rendering when redirecting
            return ''

        if self.layout is None:
            layout = zope.component.queryMultiAdapter(
                (self, self.request, self.context),
                ILayoutTemplate)
            if layout is None:
                layout = zope.component.getMultiAdapter(
                    (self, self.request), ILayoutTemplate)
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

        if self.request.response.getStatus() in REDIRECT_STATUS_CODES:
            # don't bother rendering when redirecting
            return ''

        if self.layout is None:
            layout = zope.component.queryMultiAdapter(
                (self, self.request, self.context),
                ILayoutTemplate)
            if layout is None:
                layout = zope.component.getMultiAdapter(
                    (self, self.request), ILayoutTemplate)
            return layout(self)
        return self.layout()
