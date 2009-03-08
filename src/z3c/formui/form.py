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

import zope.component
from z3c.form import form
from z3c.formui import layout
from z3c.template.interfaces import IContentTemplate

# offer built in layout support
extends = form.extends
applyChanges = form.applyChanges


class ContentTemplateMixin(object):
    """Use IContentTemplate instead of IPageTemplate.

    This prevents us running into a recusrion because of mess up layout and
    content templates. This is the default template interface if you use the
    z3c.template directive.
    """

    def render(self):
        '''See interfaces.IForm'''
        # render content template
        if self.template is None:
            template = zope.component.queryMultiAdapter(
                (self, self.request, self.context),
                IContentTemplate)
            if template is None:
                template = zope.component.getMultiAdapter(
                    (self, self.request), IContentTemplate)
            return template(self)
        return self.template()


class BaseForm(ContentTemplateMixin, layout.FormLayoutSupport, form.BaseForm):
    """Layout aware base form."""


class DisplayForm(ContentTemplateMixin, layout.FormLayoutSupport,
    form.DisplayForm):
    """Layout aware display form."""


class Form(ContentTemplateMixin, layout.FormLayoutSupport, form.Form):
    """Layout aware form."""


class AddForm(ContentTemplateMixin, layout.AddFormLayoutSupport, form.AddForm):
    """Layout aware add form."""


class EditForm(ContentTemplateMixin, layout.FormLayoutSupport, form.EditForm):
    """Layout aware edit form."""
