from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from .models import XMoneyObj, XUserExInfo

class XAdminLoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput())

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.form_method = 'post'

    self.helper.layout = Layout(
      Row(
        Column('username', css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5')
      ),
      HTML(
        """
        {% load static %}
        <div class="row" style="padding:0px; margin:0px;">
          <img src="{% static 'XMoneyRe/images/seperating-line.png' %}" class="img-fluid" style="height: 3rem; width: 100%">
        </div>
        """
      ),
      Row(
        Column('password', css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5')
      ),
      HTML(
        """
        {% load static %}
        <div class="row" style="padding:0px; margin:0px;">
          <img src="{% static 'XMoneyRe/images/seperating-line.png' %}" class="img-fluid" style="height: 3rem; width: 100%">
        </div>
        """
      ),
      Row(
        Column(
          Submit(
            'submit',
            'Submit',
            css_class = 'submit-button'
          ),
          css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5 mt-2 mb-2'
        )
      )
    )

class XUserExInfoForm(forms.ModelForm):
  headportrait_image = forms.ImageField(label='headportrait_image')
  class Meta:
    model = XUserExInfo
    fields = ('headportrait_image',)
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.form_method = 'post'

    self.helper.layout = Layout(
      Row(
        Column('headportrait_image', css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5')
      ),
      HTML(
        """
        {% load static %}
        <div class="row" style="padding:0px; margin:0px;">
          <img src="{% static 'XMoneyRe/images/seperating-line.png' %}" class="img-fluid" style="height: 2rem; width: 100%">
        </div>
        """
      ),
      Row(
        Column(
          Submit(
            'submit',
            'Submit',
            css_class = 'submit-button'
          ),
          css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5 mt-1'
        )
      )
    )

class XMOImageForm(forms.ModelForm):
  image = forms.ImageField(label='image')
  class Meta:
    model = XMoneyObj
    fields = ('image',)
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.form_method = 'post'

    self.helper.layout = Layout(
      Row(
        Column('image', css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5')
      ),
      HTML(
        """
        {% load static %}
        <div class="row" style="padding:0px; margin:0px;">
          <img src="{% static 'XMoneyRe/images/seperating-line.png' %}" class="img-fluid" style="height: 2rem; width: 100%">
        </div>
        """
      ),
      Row(
        Column(
          Submit(
            'submit',
            'Submit',
            css_class = 'submit-button'
          ),
          css_class='col-12 col-md-12 col-sm-12 col-lg-12 col-xl-12 pl-5 pr-5 mt-1'
        )
      )
    )