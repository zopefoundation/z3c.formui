====================
Form User Interfaces
====================

This package provides several useful templates to get a quick start with the
``z3c.form`` package. Previous form frameworks always included default
templates that were implemented in a particular user-interface development
pattern. If you wanted to use an alternative strategy to develop user
interfaces, it was often tedious to do so. This package aims to provide some
options without requiring them for the basic framework.


Layout Template Support
-----------------------

One common pattern in Zope 3 user interface development is the use of layout
templates (see z3c.template). This package provides some mixin classes to the
regular form classes to support layout-based templating.

  >>> from z3c.form import testing
  >>> testing.setupFormDefaults()

Before we can start writing forms, we must have the content to work with:

  >>> import zope.interface
  >>> import zope.schema
  >>> class IPerson(zope.interface.Interface):
  ...
  ...     name = zope.schema.TextLine(
  ...         title=u'Name',
  ...         required=True)
  ...
  ...     age = zope.schema.Int(
  ...         title=u'Age',
  ...         description=u"The person's age.",
  ...         min=0,
  ...         default=20,
  ...         required=False)

  >>> from zope.schema.fieldproperty import FieldProperty
  >>> class Person(object):
  ...     zope.interface.implements(IPerson)
  ...
  ...     name = FieldProperty(IPerson['name'])
  ...     age = FieldProperty(IPerson['age'])
  ...
  ...     def __init__(self, name, age):
  ...         self.name = name
  ...         self.age = age
  ...
  ...     def __repr__(self):
  ...         return '<%s %r>' % (self.__class__.__name__, self.name)

Okay, that should suffice for now. Let's now create a working add form:

  >>> from z3c.form import field
  >>> from z3c.formui import form, layout
  >>> class PersonAddForm(form.AddForm):
  ...
  ...     fields = field.Fields(IPerson)
  ...
  ...     def create(self, data):
  ...         return Person(**data)
  ...
  ...     def add(self, object):
  ...         self.context[object.id] = object
  ...
  ...     def nextURL(self):
  ...         return 'index.html'

Let's create a request:

  >>> from z3c.form.testing import TestRequest
  >>> from zope.interface import alsoProvides
  >>> divRequest = TestRequest()

And support the div form layer for our request:

  >>> from z3c.formui.interfaces import IDivFormLayer
  >>> alsoProvides(divRequest, IDivFormLayer)

Now create the form:

  >>> addForm = PersonAddForm(root, divRequest)

Since we have not specified a template yet, we have to do this now. We use our
div based form template:

  >>> import os
  >>> import z3c.formui
  >>> divFormTemplate = os.path.join(os.path.dirname(z3c.formui.__file__),
  ...     'div-form.pt')

  >>> from z3c.template.template import TemplateFactory
  >>> divFormFactory = TemplateFactory(divFormTemplate, 'text/html')

Now register the form (content) template:

  >>> import zope.interface
  >>> import zope.component
  >>> from z3c.template.interfaces import IContentTemplate
  >>> zope.component.provideAdapter(divFormFactory,
  ...     (zope.interface.Interface, IDivFormLayer),
  ...     IContentTemplate)

And let's define a layout template which simply calls the render method. For a
more advanced content/layout render concept see z3c.pagelet.

  >>> import tempfile
  >>> temp_dir = tempfile.mkdtemp()

  >>> myLayout = os.path.join(temp_dir, 'myLayout.pt')
  >>> open(myLayout, 'w').write('''<html>
  ...   <body>
  ...     <tal:block content="structure view/render">
  ...       content
  ...     </tal:block>
  ...   </body>
  ... </html>''')
  >>> myLayoutFactory = TemplateFactory(myLayout, 'text/html')

  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> zope.component.provideAdapter(myLayoutFactory,
  ...     (zope.interface.Interface, zope.interface.Interface), ILayoutTemplate)

Now we can get our layout template:

  >>> layout = zope.component.getMultiAdapter((addForm, divRequest),
  ...     ILayoutTemplate)

  >>> layout.__class__.__name__
  'ViewPageTemplateFile'

  >>> os.path.basename(layout.filename)
  'myLayout.pt'


DIV-based Layout
----------------

Let's now render the page. Note the output doesn't contain the layout template:

  >>> addForm.update()
  >>> print addForm.render()
  <form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data" class="edit-form"
          name="form" id="form">
    <div class="viewspace">
      <div class="required-info">
        <span class="required">*</span> &ndash; required
      </div>
      <div>
        <div id="form-widgets-name-row" class="row">
          <div class="label">
            <label for="form-widgets-name">
              <span>Name</span>
              <span class="required">*</span>
            </label>
          </div>
          <div class="widget"><input type="text" id="form-widgets-name"
                   name="form.widgets.name"
                   class="text-widget required textline-field" value="" />
          </div>
        </div>
        <div id="form-widgets-age-row" class="row">
          <div class="label">
            <label for="form-widgets-age">
              <span>Age</span>
            </label>
          </div>
          <div class="widget"><input type="text" id="form-widgets-age"
                   name="form.widgets.age" class="text-widget int-field"
                   value="20" />
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="buttons">
        <input type="submit" id="form-buttons-add"
               name="form.buttons.add"
               class="submit-widget button-field" value="Add" />
      </div>
    </div>
  </form>

But we can call our form which uses the new layout template which renders
the form within the div-form content template:

  >>> print addForm()
  <html>
    <body>
      <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        name="form" id="form">
        <div class="viewspace">
          <div class="required-info">
            <span class="required">*</span>
            &ndash; required
          </div>
          <div>
            <div id="form-widgets-name-row" class="row">
              <div class="label">
                <label for="form-widgets-name">
                  <span>Name</span>
                  <span class="required">*</span>
                </label>
              </div>
              <div class="widget"><input type="text" id="form-widgets-name"
                   name="form.widgets.name"
                   class="text-widget required textline-field" value="" />
              </div>
            </div>
            <div id="form-widgets-age-row" class="row">
              <div class="label">
                <label for="form-widgets-age">
                  <span>Age</span>
                </label>
              </div>
              <div class="widget"><input type="text" id="form-widgets-age"
                   name="form.widgets.age" class="text-widget int-field"
                   value="20" />
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="buttons">
            <input type="submit" id="form-buttons-add"
             name="form.buttons.add"
             class="submit-widget button-field" value="Add" />
          </div>
        </div>
      </form>
    </body>
  </html>


Table-based Forms
-----------------

There is a table based layout too. Let's define the template and use them:

  >>> from z3c.formui.interfaces import ITableFormLayer
  >>> tableFormTemplate = os.path.join(os.path.dirname(z3c.formui.__file__),
  ...     'table-form.pt')

  >>> from z3c.template.template import TemplateFactory
  >>> tableFormFactory = TemplateFactory(tableFormTemplate, 'text/html')

Now register the form (content) template:

  >>> zope.component.provideAdapter(tableFormFactory,
  ...     (zope.interface.Interface, ITableFormLayer), IContentTemplate)

Patch the request and call the form again:

  >>> tableRequest = TestRequest()
  >>> alsoProvides(tableRequest, ITableFormLayer)

Now our new request should know the table based form template:

  >>> addForm = PersonAddForm(root, tableRequest)
  >>> print addForm()
  <html>
    <body>
      <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        name="form" id="form">
        <div class="viewspace">
          <div class="required-info">
            <span class="required">*</span>
            &ndash; required
          </div>
          <div>
          <table class="form-fields">
                <tr class="row">
                  <td class="label">
                    <label for="form-widgets-name">
                      <span>Name</span>
                      <span class="required"> * </span>
                    </label>
                  </td>
                  <td class="field">
                    <div class="widget"><input type="text" id="form-widgets-name"
                         name="form.widgets.name"
                         class="text-widget required textline-field" value="" />
                    </div>
                  </td>
                </tr>
                <tr class="row">
                  <td class="label">
                    <label for="form-widgets-age">
                      <span>Age</span>
                    </label>
                  </td>
                  <td class="field">
                    <div class="widget"><input type="text" id="form-widgets-age"
                         name="form.widgets.age" class="text-widget int-field"
                         value="20" />
                    </div>
                  </td>
                </tr>
          </table>
        </div>
      </div>
      <div>
        <div class="buttons">
          <input type="submit" id="form-buttons-add"
         name="form.buttons.add"
         class="submit-widget button-field" value="Add" />
        </div>
      </div>
      </form>
    </body>
  </html>


`AddForm` rendering for `IAdding`
---------------------------------

The `z3c.formui` package also provides a layout-aware version of
`z3c.form.adding.AddForm` which can be used for creating forms for the
`zope.app.container.interfaces.IAdding` mechanism.

Let's check its template support. First, create the form for an `Adding`
instance. We just need to define the ``create()`` method, because the default
``add()`` and ``nextURL()`` methods are already defined using the `Adding`
object.

  >>> from z3c.formui import adding
  >>> class AddingPersonAddForm(adding.AddForm):
  ...
  ...     fields = field.Fields(IPerson)
  ...
  ...     def create(self, data):
  ...         return Person(**data)


Let's now instantiate the adding component and the add form:

  >>> from zope.app.container.browser.adding import Adding
  >>> rootAdding = Adding(root, divRequest)

  >>> addForm = AddingPersonAddForm(rootAdding, divRequest)

First, let's ensure that we can lookup a layout template for the form:

  >>> layout = zope.component.getMultiAdapter(
  ...     (addForm, divRequest), ILayoutTemplate)

  >>> layout.__class__.__name__
  'ViewPageTemplateFile'

Okay, that worked. Let's now render the div-based addform:

  >>> print addForm()
  <html>
    <body>
      <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        name="form" id="form">
        <div class="viewspace">
          <div class="required-info">
            <span class="required">*</span>
            &ndash; required
          </div>
          <div>
            <div id="form-widgets-name-row" class="row">
              <div class="label">
                <label for="form-widgets-name">
                  <span>Name</span>
                  <span class="required">*</span>
                </label>
              </div>
              <div class="widget"><input type="text" id="form-widgets-name"
                   name="form.widgets.name"
                   class="text-widget required textline-field" value="" />
              </div>
            </div>
            <div id="form-widgets-age-row" class="row">
              <div class="label">
                <label for="form-widgets-age">
                  <span>Age</span>
                </label>
              </div>
              <div class="widget"><input type="text" id="form-widgets-age"
                   name="form.widgets.age" class="text-widget int-field"
                   value="20" />
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="buttons">
            <input type="submit" id="form-buttons-add"
             name="form.buttons.add"
             class="submit-widget button-field" value="Add" />
          </div>
        </div>
      </form>
    </body>
  </html>

Okay, now we are going to check table layout support.

  >>> rootAdding = Adding(root, tableRequest)
  >>> addForm = AddingPersonAddForm(rootAdding, tableRequest)

Again, the layout should be available:

  >>> layout = zope.component.getMultiAdapter((addForm, tableRequest),
  ...     ILayoutTemplate)

  >>> layout.__class__.__name__
  'ViewPageTemplateFile'

Let's now render the form:

  >>> print addForm()
  <html>
    <body>
      <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        name="form" id="form">
        <div class="viewspace">
          <div class="required-info">
            <span class="required">*</span>
            &ndash; required
          </div>
          <div>
          <table class="form-fields">
                <tr class="row">
                  <td class="label">
                    <label for="form-widgets-name">
                      <span>Name</span>
                      <span class="required"> * </span>
                    </label>
                  </td>
                  <td class="field">
                    <div class="widget"><input type="text" id="form-widgets-name"
                         name="form.widgets.name"
                         class="text-widget required textline-field" value="" />
                    </div>
                  </td>
                </tr>
                <tr class="row">
                  <td class="label">
                    <label for="form-widgets-age">
                      <span>Age</span>
                    </label>
                  </td>
                  <td class="field">
                    <div class="widget"><input type="text" id="form-widgets-age"
                         name="form.widgets.age" class="text-widget int-field"
                         value="20" />
                    </div>
                  </td>
                </tr>
          </table>
        </div>
      </div>
      <div>
        <div class="buttons">
          <input type="submit" id="form-buttons-add"
         name="form.buttons.add"
         class="submit-widget button-field" value="Add" />
        </div>
      </div>
      </form>
    </body>
  </html>


Form Macros
-----------

Load the configuration, which will make sure that all macros get registered
correctly:

  >>> from zope.configuration import xmlconfig
  >>> import zope.component
  >>> import zope.viewlet
  >>> import zope.app.component
  >>> import zope.app.publisher.browser
  >>> import z3c.macro
  >>> import z3c.template
  >>> import z3c.formui
  >>> xmlconfig.XMLConfig('meta.zcml', zope.component)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.viewlet)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.app.component)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.app.publisher.browser)()
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.macro)()
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.template)()
  >>> xmlconfig.XMLConfig('configure.zcml', z3c.formui)()

Div IContentTemplate
--------------------

Create some dummy form discriminators for calling div layout templates and
macros and check the div IContentTemplates:

  >>> objects = (addForm, divRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate).filename
  '...div-form.pt'

  >>> objects = (form.DisplayForm(None, None), divRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate, '').filename
  '...div-form-display.pt'

We offer the following named IContentTemplate:

  >>> objects = (form.DisplayForm(None, None), divRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate,
  ...     'display').filename
  '...div-form-display.pt'

  >>> objects = (form.DisplayForm(None, None), divRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate,
  ...     'subform').filename
  '...subform.pt'


Table ILayoutTemplate
---------------------

There is one generic layout template to build sub forms:

  >>> objects = (form.DisplayForm(None, None), divRequest)
  >>> zope.component.getMultiAdapter(objects, ILayoutTemplate,
  ...     'subform').filename
  '...subform-layout.pt'


Div layout macros
-----------------

We have different form macros available for IInputForm:


  >>> from z3c.macro.interfaces import IMacroTemplate
  >>> objects = (None, addForm, divRequest)
  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form')
  [...div-form.pt'), ...metal:define-macro': u'form'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'subform')
  [...div-form.pt'), ...define-macro': u'subform'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-label')
  [...div-form.pt'), ...define-macro': u'label'...


  >>> zope.component.getMultiAdapter(
  ...     objects, IMacroTemplate, 'form-required-info')
  [...div-form.pt'), ...define-macro', u'required-info'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-header')
  [...div-form.pt'), ...define-macro': u'header'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-errors')
  [...div-form.pt'), ...define-macro': u'errors'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'widget-rows')
  [...div-form.pt'), ...define-macro': u'widget-rows'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'widget-row')
  [...div-form.pt'), ...define-macro': u'widget-row'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-groups')
  [...div-form.pt'), ...define-macro': u'groups'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-buttons')
  [...div-form.pt'), ...define-macro', u'buttons'...


And we have different form macros available for IDisplayForm:

  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'subform-display')
  [...div-form-display.pt'), ...define-macro': u'subform-display'...


Table IContentTemplate
----------------------

Create some dummy form discriminators for calling table layout templates and
macros and check the div IContentTemplates:

  >>> objects = (addForm, tableRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate, '').filename
  '...table-form.pt'

  >>> objects = (form.DisplayForm(None, None), tableRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate, '').filename
  '...table-form-display.pt'

We offer the following named IContentTemplate:

  >>> objects = (form.DisplayForm(None, None), tableRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate,
  ...     'display').filename
  '...table-form-display.pt'

  >>> objects = (form.DisplayForm(None, None), tableRequest)
  >>> zope.component.getMultiAdapter(objects, IContentTemplate,
  ...     'subform').filename
  '...subform.pt'



Table ILayoutTemplate
---------------------

There is one generic layout template to build sub forms:

  >>> objects = (form.DisplayForm(None, None), tableRequest)
  >>> zope.component.getMultiAdapter(objects, ILayoutTemplate,
  ...     'subform').filename
  '...subform-layout.pt'


Table layout macros
-------------------

We have different form macros available for IInputForm:

  >>> objects = (None, addForm, tableRequest)
  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form')
  [...table-form.pt'), ...metal:define-macro': u'form'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'subform')
  [...table-form.pt'), ...define-macro': u'subform'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-label')
  [...table-form.pt'), ...define-macro': u'label'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-required-info')
  [...table-form.pt'), ...define-macro', u'required-info'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-header')
  [...table-form.pt'), ...define-macro': u'header'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-errors')
  [...table-form.pt'), ...define-macro': u'errors'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-table')
  [...table-form.pt'), ...define-macro', u'formtable'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-row')
  [...table-form.pt'), ...define-macro': u'formrow'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-label-cell')
  [...table-form.pt'), ...define-macro', u'labelcell'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-widget-cell')
  [...table-form.pt'), ...define-macro', u'widgetcell'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-groups')
  [...table-form.pt'), ...define-macro': u'groups'...


  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'form-buttons')
  [...table-form.pt'), ...define-macro', u'buttons'...


And we have different form macros available for IDisplayForm:

  >>> zope.component.getMultiAdapter(objects, IMacroTemplate, 'subform-display')
  [...table-form-display.pt'), ...define-macro': u'subform-display'...


Subform
-------

Let's give a quick overview how subform content and layout templates get used:
First define a new form which uses the template getter methods offered
from z3.template

  >>> from z3c.template.template import getPageTemplate
  >>> from z3c.template.template import getLayoutTemplate

The ``provider`` TALES expression which is a part of the lookup concept
was already registered by the testing setup, so we don't need to do it
here.

and the TALES expression called ``macro`` which can lookup our macro adapters.
Yes, macros are adapters in our content/layout template concept. See z3c.macro
for more information about the implementation. However, we already registered
the ``macro`` type in the testing setup, as it's needed for rendering form
templates.

and at least we need a pagelet
renderer. By default we use the provider called ``PageletRenderer`` defined
in the z3c.pagelet package. But right now, we don't have a dependency on
this package. So let's implement a simple renderer and use them as a
IContentProvider:

  >>> class PageletRenderer(object):
  ...     zope.component.adapts(zope.interface.Interface,
  ...         zope.publisher.interfaces.browser.IBrowserRequest,
  ...         zope.interface.Interface)
  ...
  ...     def __init__(self, context, request, pagelet):
  ...         self.__updated = False
  ...         self.__parent__ = pagelet
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def update(self):
  ...         pass
  ...
  ...     def render(self):
  ...         return self.__parent__.render()

  >>> from zope.contentprovider.interfaces import IContentProvider
  >>> zope.component.provideAdapter(PageletRenderer,
  ...     provides=IContentProvider, name='pagelet')

Now define the form:

  >>> class PersonEditForm(form.EditForm):
  ...     """Edit form including layout support. See z3c.formui.form."""
  ...
  ...     template = getPageTemplate('subform')
  ...     layout = getLayoutTemplate('subform')
  ...
  ...     fields = field.Fields(IPerson)

Now we can render the form with our previous created person instance:

  >>> person = Person(u'Jessy', 6)
  >>> editForm = PersonEditForm(person, divRequest)

Now we call the form which will update and render it:

  >>> print editForm()
  <div class="viewspace">
    <div class="required-info">
      <span class="required">*</span>
      &ndash; required
    </div>
    <div>
      <div id="form-widgets-name-row" class="row">
        <div class="label">
          <label for="form-widgets-name">
            <span>Name</span>
            <span class="required">*</span>
          </label>
        </div>
        <div class="widget"><input type="text" id="form-widgets-name"
             name="form.widgets.name"
             class="text-widget required textline-field"
             value="Jessy" />
        </div>
      </div>
      <div id="form-widgets-age-row" class="row">
        <div class="label">
          <label for="form-widgets-age">
            <span>Age</span>
          </label>
        </div>
        <div class="widget"><input type="text" id="form-widgets-age"
           name="form.widgets.age" class="text-widget int-field"
           value="6" />
        </div>
      </div>
    </div>
  </div>
  <div>
    <div class="buttons">
      <input type="submit" id="form-buttons-apply"
             name="form.buttons.apply"
             class="submit-widget button-field" value="Apply" />
    </div>
  </div>

You can see that the form above is a real subform. It doesn't define the form
tag which makes it usable as a subform in parent forms.

Of course this works with table layout based forms too. Let's use our table
request and render the form again:

  >>> editForm = PersonEditForm(person, tableRequest)
  >>> print editForm()
  <div class="viewspace">
    <div class="required-info">
      <span class="required">*</span>
      &ndash; required
    </div>
    <div>
      <table class="form-fields">
        <tr class="row">
          <td class="label">
            <label for="form-widgets-name">
              <span>Name</span>
              <span class="required"> * </span>
            </label>
          </td>
          <td class="field">
            <div class="widget"><input type="text" id="form-widgets-name"
                 name="form.widgets.name"
                 class="text-widget required textline-field"
                 value="Jessy" />
            </div>
          </td>
        </tr>
        <tr class="row">
          <td class="label">
            <label for="form-widgets-age">
              <span>Age</span>
            </label>
          </td>
          <td class="field">
            <div class="widget"><input type="text" id="form-widgets-age"
                 name="form.widgets.age" class="text-widget int-field"
                 value="6" />
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>
  <div>
    <div class="buttons">
      <input type="submit" id="form-buttons-apply"
             name="form.buttons.apply"
            class="submit-widget button-field" value="Apply" />
    </div>
  </div>

Redirection
-----------

The form doesn't bother rendering itself and its layout when
request is a redirection as the rendering doesn't make any sense with
browser requests in that case. Let's create a view that does a
redirection in its update method:

 >>> class RedirectingView(PersonEditForm):
 ...     def update(self):
 ...         super(RedirectingView, self).update()
 ...         self.request.response.redirect('.')

It will return an empty string when called as a browser page.

 >>> redirectView = RedirectingView(person, divRequest)
 >>> redirectView() == ''
 True

However, the ``render`` method will render form's template as usual:

 >>> '<div class="viewspace">' in redirectView.render()
 True

The same thing should work for AddForms:

 >>> class RedirectingAddView(PersonAddForm):
 ...     def update(self):
 ...         super(RedirectingAddView, self).update()
 ...         self.request.response.redirect('.')
 >>> redirectView = RedirectingAddView(person, divRequest)
 >>> redirectView() == ''
 True

No required fields
------------------

If there no required fields in the form, standard templates won't render
the "required-info" hint.

  >>> class IAdditionalInfo(zope.interface.Interface):
  ...
  ...     location = zope.schema.TextLine(title=u'Location', required=False)
  ...     about = zope.schema.Text(title=u'About', required=False)  

  >>> class AdditionalInfoForm(form.AddForm):
  ...
  ...     fields = field.Fields(IAdditionalInfo)
  
  >>> additionalInfoForm = AdditionalInfoForm(root, divRequest)
  >>> additionalInfoForm.update()
  >>> '<div class="required-info">' in additionalInfoForm.render()
  False

  >>> additionalInfoForm = AdditionalInfoForm(root, tableRequest)
  >>> additionalInfoForm.update()
  >>> '<div class="required-info">' in additionalInfoForm.render()
  False

Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)
