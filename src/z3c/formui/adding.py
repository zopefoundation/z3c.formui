##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
"""Implementation of layout-aware addform for IAdding

$Id:$
"""
__docformat__ = "reStructuredText"

from z3c.form import adding
from z3c.formui import form, layout

class AddForm(form.ContentTemplateMixin, layout.AddFormLayoutSupport,
              adding.AddForm):
    """Layout aware add form for zope.app.container.interfaces.IAdding."""
