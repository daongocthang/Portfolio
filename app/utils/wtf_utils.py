from markupsafe import Markup
from wtforms import Field
from wtforms.widgets.core import html_params, escape


class InlineButtonWidget(object):
    def __init__(self, class_=None):
        self.class_ = class_

    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'submit')
        kwargs.setdefault('name', field.name)
        kwargs["class"] = self.class_
        params = html_params(**kwargs)

        html = '<input %s value="%s"/>'
        return Markup(html % (params, escape(field.label.text)))


class InlineButton(Field):
    widget = InlineButtonWidget()

    def __init__(self, label=None, validators=None, text='Save', **kwargs):
        super(InlineButton, self).__init__(label, validators, **kwargs)
        self.text = text

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''
