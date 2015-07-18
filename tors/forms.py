from django.forms import forms, fields
from django.utils.translation import ugettext_lazy as _l

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


class SingleButtonMixin(object):
    action_text = _l('Save')

    def __init__(self, *args, **kwargs):
        super(SingleButtonMixin, self).__init__(*args, **kwargs)
        self.helper = getattr(self, 'helper', FormHelper(self))
        self.helper.layout.append(
            FormActions(
                Submit('action', self.action_text, css_class="btn-primary"),
            )
        )


class SearchForm(SingleButtonMixin, forms.Form):
    keyword = fields.CharField(required=True)
    action_text = _l('Search')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = getattr(self, 'helper', FormHelper(self))
        self.helper.form_method = 'GET'
