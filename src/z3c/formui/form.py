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
"""Form UI Browser

$Id: browser.py 75941 2007-05-24 14:48:22Z srichter $
"""
__docformat__ = "reStructuredText"

from z3c.form import form
from z3c.formui import layout

# offer built in layout support
extends = form.extends
applyChanges = form.applyChanges


class BaseForm(layout.FormLayoutSupport, form.BaseForm):
    """Layout aware base form."""


class DisplayForm(layout.FormLayoutSupport, form.DisplayForm):
    """Layout aware display form."""


class Form(layout.FormLayoutSupport, form.Form):
    """Layout aware form."""


class AddForm(layout.AddFormLayoutSupport, form.AddForm):
    """Layout aware add form."""


class EditForm(layout.FormLayoutSupport, form.EditForm):
    """Layout aware edit form."""
