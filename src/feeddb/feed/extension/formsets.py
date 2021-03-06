"""
extended BaseInlineFormSet
"""

from django.utils.encoding import smart_unicode, force_unicode
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _, ugettext

from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, NON_FIELD_ERRORS
from django.forms.fields import Field, ChoiceField, IntegerField, EMPTY_VALUES
from django.forms.widgets import Select, SelectMultiple, HiddenInput, MultipleHiddenInput
from django.forms.widgets import media_property
from django.forms.models import BaseInlineFormSet

class PositionBaseInlineFormSet(BaseInlineFormSet):
    check_startposition=True
    check_unique=True
    check_consecutive=True
    
    def clean(self):
        form_errors = []
        errors = super(PositionBaseInlineFormSet, self).clean()
        if errors:
            form_errors.extend(errors)
        if self.forms:
            if self.forms[0].fields.has_key("position"):
                positions = []
                for f in self.forms:
                    p=f.cleaned_data.get("position", None)
                    if p != None and p!="":
                        if f.fields.has_key('DELETE'): 
                            if f._raw_value('DELETE')!="on":
                                positions.append(int(p))
                        else:
                            positions.append(int(p))
                if positions:
                    positions.sort()
                    #check start position must be 1
                    if self.check_startposition and positions[0]!=1:
                        form_errors.append("position must start from 1")
                    for i in range(1, len(positions)):
                        #check unique position
                        if self.check_unique and positions[i-1]==positions[i]:
                            form_errors.append("duplicate position: %s." % str(positions[i]))
                        #check consecutiveness
                        if self.check_consecutive and positions[i]-positions[i-1]!=1:
                            form_errors.append("positions are not consecutive between %s and %s." % (str(positions[i-1]), str(positions[i])) )
        if form_errors:
            raise ValidationError(form_errors)

class TrialInlineFormSet(PositionBaseInlineFormSet):
    check_startposition=False
    check_unique=True
    check_consecutive=False

   
class OrderedFormset(BaseInlineFormSet):
    def get_queryset(self):
        qs = super(BaseInlineFormSet, self).get_queryset()
        if hasattr(self.form, 'ordering'):
            ordering=self.form.ordering
            if not ordering in (None,''):
                return qs.order_by(ordering)
        return qs         