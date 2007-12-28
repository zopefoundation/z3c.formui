====================
Form User Interfaces
====================

This package provides several useful templates to get a quick start with the
``z3c.form`` package. Previous form frameworks always included default
templates that were implemented in a particular user-interface development
pattern. If you wanted to use an alternative strategy to develop user
interfaces, it was often tedious to do so. This package aims to provide some
options without requireing them for the basic framework.


Layout Template Support
-----------------------

One common pattern in Zope 3 user interface development is the use of layout
templates. This package provides some mixin classes to the regular form
classes to support layout-based templating.

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
more adavanced content/layout render concept see z3c.pagelet.

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

  >>> layout
  <zope.app.pagetemplate.viewpagetemplatefile.ViewPageTemplateFile object at ...>


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


Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)
