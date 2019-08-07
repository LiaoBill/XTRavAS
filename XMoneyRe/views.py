from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.conf import settings

from .models import XMoneyObj, XUserExInfo, XCurrency, XTripInfo
from .forms import XAdminLoginForm, XUserExInfoForm, XMOImageForm

from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import os

def showMainPage(request):
  # not login requirement
  # get trip day
  trip_info_object = XTripInfo.objects.order_by('object_id')[0]
  # tripday
  trip_day = trip_info_object.current_trip_day
  # get current utc
  current_utc = trip_info_object.current_utc
  str_current_utc = ""
  if int(current_utc) > 0:
    str_current_utc = "+" + str(current_utc)
  else:
    str_current_utc = str(current_utc)
  # get admin list
  admin_list = XUserExInfo.objects.order_by('username')
  context= {
    'trip_day': trip_day,
    'current_utc': str_current_utc,
    'admin_list': admin_list,
    'random_key': datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  }
  return render(request, "XMoneyRe/XMainPage.html", context)

def updateTripInfo(request):
  # login requirement
  # check login or not
  user = None
  if 'username' in request.COOKIES:
    showing_name = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=showing_name)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')
  if request.method == 'POST':
    # get trip day
    trip_info_object = XTripInfo.objects.order_by('object_id')[0]

    current_trip_day = request.POST.get('mo_trip_day')
    current_utc = request.POST.get('mo_utc')
    trip_info_object.current_trip_day = current_trip_day
    trip_info_object.current_utc = current_utc
    trip_info_object.save()
    return redirect('main_function_page')

  else:
    # get trip day
    trip_info_object = XTripInfo.objects.order_by('object_id')[0]
    # tripday
    trip_day = trip_info_object.current_trip_day
    # get current utc
    current_utc = trip_info_object.current_utc

    context= {
      'trip_day': trip_day,
      'current_utc': current_utc,
      'error_message': ""
    }
    return render(request, "XMoneyRe/XUpdateTripInfo.html", context)



def showMainFunctionPage(request):
  # check login or not
  user = None
  if 'username' in request.COOKIES:
    showing_name = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=showing_name)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')
  

  # get trip day
  trip_info_object = XTripInfo.objects.order_by('object_id')[0]
  # tripday
  trip_day = trip_info_object.current_trip_day
  # get current utc
  current_utc = trip_info_object.current_utc

  str_current_utc = ""
  if int(current_utc) > 0:
    str_current_utc = "+" + str(current_utc)
  else:
    str_current_utc = str(current_utc)
  context = {
    'showing_name': user.username,
    'trip_day': trip_day,
    'current_utc': str_current_utc,
    'is_admin': True,
    'headportrait_url': user.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  }
  return render(request, 'XMoneyRe/XMainFunctionPage.html', context)


def showMO_tripday(request, trip_day):
  # no login requeirement
  is_admin = False
  if 'username' in request.COOKIES:
    is_admin = True
  try:
    trip_day = int(trip_day)
  except:
    context = {
      'x_money_object_list': None,
      'empty_message': "url not valid",
      'trip_day': "? ? ?",
      'record_count': "? ? ?",
      'admin_list': None,
      'is_admin':is_admin
    }
    return render(request, 'XMoneyRe/XMO-Tripday.html', context)
  trip_day = str(trip_day)
  x_money_object_list = XMoneyObj.objects.filter(trip_day=trip_day).order_by('-object_id')

  current_trip_day = XTripInfo.objects.order_by('object_id')[0].current_trip_day
  # check empty or not
  empty_message = ""
  if len(x_money_object_list) == 0:
    empty_message = "Trip Day " + trip_day + " still empty (BiBo)!"

  admin_list = XUserExInfo.objects.order_by('username')
  record_count = len(x_money_object_list)

  context = {
    'x_money_object_list': x_money_object_list,
    'empty_message': empty_message,
    'trip_day': trip_day,
    'record_count': record_count,
    'admin_list': admin_list,
    'current_trip_day': current_trip_day,
    'is_admin':is_admin
  }
  return render(request, 'XMoneyRe/XMO-Tripday.html', context)


def showUserView(request, username):
  # no login requeirment
  user = None
  context = None
  try:
    user = XUserExInfo.objects.get(username=username)
  except:
    # not found
    context = {
      'username': None,
      'headportrait_url': None
    }
    return render(request, 'XMoneyRe/XUserView.html', context)
  current_trip_day = XTripInfo.objects.order_by('object_id')[0].current_trip_day
  context = {
    'username': user.username,
    'trip_day': str(current_trip_day),
    'headportrait_url': user.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  }
  return render(request, 'XMoneyRe/XUserView.html', context)


def showMO_spec(request, mo_id):

  is_admin = False
  if 'username' in request.COOKIES:
    is_admin = True
  # no login requirement
  # get trip day
  trip_info_object = XTripInfo.objects.order_by('object_id')[0]
  # tripday
  trip_day = trip_info_object.current_trip_day
  current_mo = None
  try:
    current_mo = XMoneyObj.objects.get(object_id=mo_id)
  except:
    # not get
    context = {
      'current_mo': None,
      'trip_day': trip_day,
      'empty_message': "No record for id:" + mo_id + " record!"
    }
    return render(request, 'XMoneyRe/XMO-Spec.html', context)
  # fill context and render
  admin_list = XUserExInfo.objects.order_by('username')
  creator_username = current_mo.created_by
  updator_username = current_mo.latest_updator
  creator = None
  updator = None
  is_creator_found = False
  is_updator_found = False
  for admin in admin_list:
    if admin.username == creator_username:
      creator = admin
      is_creator_found = True
    if admin.username == updator_username:
      updator = admin
      is_updator_found = True
    if is_creator_found == True and is_updator_found == True:
      break
  # get image url
  mo_image_url = None
  if current_mo.image != "":
    mo_image_url = current_mo.image.url
    # mo_image_url += "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  context = {
    'current_mo': current_mo,
    'mo_image_url': mo_image_url,
    'trip_day': trip_day,
    'is_admin': is_admin,
    # creator
    'creator_hp_url': creator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    'creator_username': creator_username,
    # updator
    'updator_hp_url': updator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    'updator_username': updator_username
  }
  return render(request, 'XMoneyRe/XMO-Spec.html', context)


# money object overview list view
def showXMoneyObj_OverviewList(request):
  # not using function
  x_money_object_list = XMoneyObj.objects.order_by('-object_id')
  context = {'x_money_object_list': x_money_object_list}
  return render(request, 'XMoneyRe/XMoneyObj-OverviewList.html', context)


def showUserCenter(request):
  # login required
  user = None
  if 'username' in request.COOKIES:
    showing_name = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=showing_name)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')
  # show
  context = {
    'username': user.username,
    'headportrait_url': user.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  }
  return render(request, 'XMoneyRe/XUserCenter.html', context)


def updateUserHeadPortrait(request):
  # login required
  user = None
  if 'username' in request.COOKIES:
    showing_name = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=showing_name)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')
  if request.method == 'POST':
    head_portrait_update_form = XUserExInfoForm(
      request.POST, request.FILES)  # , request.FILES
    if head_portrait_update_form.is_valid():
      head_portrait = head_portrait_update_form.cleaned_data['headportrait_image']

      # get username and model
      current_user_name = "NONE"
      if 'username' in request.COOKIES:
        current_user_name = request.COOKIES['username']
      else:
        # actually not gonna happen here
        head_portrait_update_form = XUserExInfoForm()
        error_information = "Internal Unknown Error Occurred!"
        context = {
          'head_portrait_update_form': head_portrait_update_form,
          'error_information': error_information
        }
        return render(request, 'XMoneyRe/XUpdateHeadPortrait.html', context)
      x_user_exinfo_model = None
      try:
        x_user_exinfo_model = XUserExInfo.objects.get(
          username=current_user_name)
      except:
        # not found current username, means database data error
        head_portrait_update_form = XUserExInfoForm()
        error_information = "Database UserExInfo Table Data Error!"
        context = {
          'head_portrait_update_form': head_portrait_update_form,
          'error_information': error_information
        }
        return render(request, 'XMoneyRe/XUpdateHeadPortrait.html', context)

      # check whether process will work
      image = Image.open(head_portrait.file.name)
      width, height = image.size
      target_width = 100
      target_height = 100
      if width < target_width or height < target_height:
        # image not valid
        head_portrait_update_form = XUserExInfoForm()
        error_information = "Head Portrait must bigger than 100X100!"
        context = {
          'head_portrait_update_form': head_portrait_update_form,
          'error_information': error_information
        }
        return render(request, 'XMoneyRe/XUpdateHeadPortrait.html', context)

      # delete previous picture part
      remove_hp_name = current_user_name + \
        "_headportrait-" + x_user_exinfo_model.previous_tag
      # remove previous image file on disk
      try:
        os.remove(os.path.join(settings.MEDIA_ROOT +
                     settings.MEDIA_HEADPORTRAIT_PLACE, remove_hp_name))
      except:
        # delete not success
        head_portrait_update_form = XUserExInfoForm()
        error_information = "Disk HeadPortrait Delete Not Success!"
        context = {
          'head_portrait_update_form': head_portrait_update_form,
          'error_information': error_information
        }
        return render(request, 'XMoneyRe/XUpdateHeadPortrait.html', context)
      # definitely deleted

      # save new image
      # get postfix_name
      last_dot_position = head_portrait.name.rfind('.')
      picture_postfix_name = head_portrait.name[last_dot_position:]
      # get datetime as unique id
      unique_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
      # set new unique id
      x_user_exinfo_model.previous_tag = unique_id + picture_postfix_name
      head_portrait.name = current_user_name + \
        "_headportrait-" + unique_id + picture_postfix_name
      # save to disk and sync database
      x_user_exinfo_model.headportrait = head_portrait
      x_user_exinfo_model.save()

      # process head portrait
      hp_name = x_user_exinfo_model.username + \
        "_headportrait-" + x_user_exinfo_model.previous_tag
      head_portrait_path = os.path.join(settings.MEDIA_ROOT +
                        settings.MEDIA_HEADPORTRAIT_PLACE, hp_name)
      image = Image.open(head_portrait_path)
      width, height = image.size
      target_width = 100
      target_height = 100
      # resize
      if width >= height:
        image = image.resize(
          (int(width/height*target_width), target_height), Image.ANTIALIAS)
      else:
        image = image.resize(
          (target_width, int(height/width*target_height)), Image.ANTIALIAS)
      width, height = image.size
      # corp
      x = int((width - target_width)/2)
      y = int((height - target_height)/2)
      x_ending = x + target_width
      y_ending = y + target_height
      image = image.crop((x, y, x_ending, y_ending))
      image.save(head_portrait_path, format=image.format, quality=100)
      # redirect to user center
      return redirect('user_center')
    else:
      head_portrait_update_form = XUserExInfoForm()
      error_information = "Data not Valid Internal Error!"
      context = {
        'head_portrait_update_form': head_portrait_update_form,
        'error_information': error_information
      }
      return render(request, 'XMoneyRe/XUpdateHeadPortrait.html', context)
  else:
    if 'username' in request.COOKIES:
      # logined
      head_portrait_update_form = XUserExInfoForm()
      context = {
        'head_portrait_update_form': head_portrait_update_form,
        'error_information': ""
      }
      return render(request, 'XMoneyRe/XUpdateHeadPortrait.html', context)
    else:
      # redirect to login page
      return redirect('admin_login')

# admin login view


def admin_login(request):
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    admin_login_form = XAdminLoginForm(request.POST)
    # check whether it's valid:
    if admin_login_form.is_valid():
      # process the data in form.cleaned_data as required
      username = admin_login_form.cleaned_data['username']
      password = admin_login_form.cleaned_data['password']

      user = authenticate(username=username, password=password)
      if user is not None:
        # set cookie
        # redirect to other pages
        showing_name = username
        user = None
        try:
          user = XUserExInfo.objects.get(username=showing_name)
        except:
          # not login or cookie error
          # redirect to login page
          return redirect('admin_login')
        # get trip day
        trip_info_object = XTripInfo.objects.order_by('object_id')[0]
        # tripday
        trip_day = trip_info_object.current_trip_day
        # get current utc
        current_utc = trip_info_object.current_utc

        str_current_utc = ""
        if int(current_utc) > 0:
          str_current_utc = "+" + str(current_utc)
        else:
          str_current_utc = str(current_utc)
        context = {
          'showing_name': showing_name,
          'trip_day': trip_day,
          'current_utc': str_current_utc,
          'is_admin': True,
          'headportrait_url': user.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        }
        response = render(
          request, 'XMoneyRe/XMainFunctionPage.html', context)
        response.set_cookie(key='username', value=username)
        return response
      else:
        admin_login_form = XAdminLoginForm()
        return render(request, 'XMoneyRe/XAdminLogin.html', {'admin_login_form': admin_login_form, 'login_feedback': "AuTHeNtiCaTIOn ErROr"})
  # if a GET (or any other method) we'll create a blank form
  else:
    if 'username' in request.COOKIES:
      return redirect('main_function_page')
    else:
      admin_login_form = XAdminLoginForm()
      return render(request, 'XMoneyRe/XAdminLogin.html', {'admin_login_form': admin_login_form, 'login_feedback': ""})

# admin logout


def admin_logout(request):

  if 'username' in request.COOKIES:
    # not login requirement
    # get trip day
    trip_info_object = XTripInfo.objects.order_by('object_id')[0]
    # tripday
    trip_day = trip_info_object.current_trip_day
    # get current utc
    current_utc = trip_info_object.current_utc
    str_current_utc = ""
    if int(current_utc) > 0:
      str_current_utc = "+" + str(current_utc)
    else:
      str_current_utc = str(current_utc)
    # get admin list
    admin_list = XUserExInfo.objects.order_by('username')
    context= {
      'trip_day': trip_day,
      'current_utc': str_current_utc,
      'admin_list': admin_list,
      'random_key': datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    }
    response = render(request, "XMoneyRe/XMainPage.html", context)
    response.delete_cookie(key='username')
    return response
  else:
    return redirect('show_main_page')

# head portrait rotation


def headportrait_rotate_left(request):
  user = None
  if 'username' in request.COOKIES:
    username = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=username)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')
  # read and operate image file
  hp_name = user.username + "_headportrait-" + user.previous_tag
  head_portrait_path = os.path.join(settings.MEDIA_ROOT +
                    settings.MEDIA_HEADPORTRAIT_PLACE, hp_name)
  image = Image.open(head_portrait_path)
  image = image.rotate(-90)
  image.save(head_portrait_path, format=image.format, quality=100)

  # rename file-not gonna work
  # remove_hp_name = user.username + "_headportrait-" + user.previous_tag
  # picture_postfix_name = user.previous_tag[(user.previous_tag.rfind('.')):]
  # unique_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  # new_hp_name = user.username + "_headportrait-" + unique_id + picture_postfix_name
  # os.rename(os.path.join(settings.MEDIA_ROOT + settings.MEDIA_HEADPORTRAIT_PLACE, remove_hp_name),
  #           os.path.join(settings.MEDIA_ROOT + settings.MEDIA_HEADPORTRAIT_PLACE, new_hp_name))
  # user.previous_tag = unique_id + picture_postfix_name
  # user.headportrait.name = new_hp_name
  # user.save()

  return redirect('user_center')


def headportrait_rotate_right(request):
  user = None
  if 'username' in request.COOKIES:
    username = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=username)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')
  hp_name = user.username + "_headportrait-" + user.previous_tag
  head_portrait_path = os.path.join(settings.MEDIA_ROOT +
                    settings.MEDIA_HEADPORTRAIT_PLACE, hp_name)
  image = Image.open(head_portrait_path)
  image = image.rotate(90)
  image.save(head_portrait_path, format=image.format, quality=100)
  return redirect('user_center')


def addMoneyObject(request):
  if request.method == 'POST':
    # get username and user
    user = None
    if 'username' in request.COOKIES:
      username = request.COOKIES['username']
      try:
        user = XUserExInfo.objects.get(username=username)
      except:
        # not login or cookie error
        # redirect to login page
        return redirect('admin_login')
    else:
      return redirect('admin_login')

    # get currency unit table
    currency_unit_list = XCurrency.objects.order_by('object_id')

    name = request.POST.get('mo_name')
    price = request.POST.get('mo_price')
    currency_unit = request.POST.get('mo_currency_unit')
    source = request.POST.get('mo_source')
    category = request.POST.get('mo_category')

    # check null
    if name == "" or price == "" or currency_unit == "" or source == "" or category == "":
      context = {
        'username': user.username,
        'headportrait_url': user.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
        'currency_unit_list': currency_unit_list,
        'addmo_feedback': "all fields should be filled!"
      }
      return render(request, 'XMoneyRe/XAddMoneyObject.html', context)

    # description empty suru
    description = "测试用description"
    # date related
    trip_info_object = XTripInfo.objects.order_by('object_id')[0]
    # tripday
    trip_day = trip_info_object.current_trip_day
    # for local datetime
    local_date = (datetime.utcnow(
    ) + timedelta(hours=int(trip_info_object.current_utc))).strftime('%Y-%m-%d-%H-%M-%S')

    # user related
    created_by = user.username
    latest_updator = user.username

    creating_object = XMoneyObj()
    creating_object.name = name
    creating_object.price = price
    creating_object.currency_unit = currency_unit
    creating_object.description = description
    creating_object.category = category
    creating_object.source = source
    creating_object.trip_day = trip_day
    creating_object.local_date = local_date
    creating_object.created_by = created_by
    creating_object.latest_updator = latest_updator

    # save current object, SQL insert executed
    creating_object.save()

    return redirect('main_function_page')

  else:
    # render adding page
    user = None
    if 'username' in request.COOKIES:
      showing_name = request.COOKIES['username']
      try:
        user = XUserExInfo.objects.get(username=showing_name)
      except:
        # not login or cookie error
        # redirect to login page
        return redirect('admin_login')

      # get currency unit table
      currency_unit_list = XCurrency.objects.order_by('object_id')
      context = {
        'username': user.username,
        'headportrait_url': user.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
        'currency_unit_list': currency_unit_list,
        'addmo_feedback': ""
      }
      return render(request, 'XMoneyRe/XAddMoneyObject.html', context)
    else:
      return redirect('admin_login')


def updateMoneyObject(request, mo_id):
  if request.method == 'POST':
    # get curret user
    user = None
    if 'username' in request.COOKIES:
      username = request.COOKIES['username']
      try:
        user = XUserExInfo.objects.get(username=username)
      except:
        # not login or cookie error
        # redirect to login page
        return redirect('admin_login')
    else:
      return redirect('admin_login')

    # get current money object
    current_mo = None
    try:
      current_mo = XMoneyObj.objects.get(object_id=mo_id)
    except:
      # not get
      return redirect('show_mo_spec', mo_id)

    # get all parts
    name = request.POST.get('mo_name')
    price = request.POST.get('mo_price')
    currency_unit = request.POST.get('mo_currency_unit')
    description = request.POST.get('mo_description')
    category = request.POST.get('mo_category')[len("For: "):]
    source = request.POST.get('mo_source')[len("From: "):]
    trip_day = request.POST.get('mo_trip_day')[len("Tripday: "):]
    local_date = request.POST.get('mo_local_time')[
      len("Local Date: "):].strip()
    latest_updator = user.username

    # get admin_list
    admin_list = XUserExInfo.objects.order_by('username')
    creator_username = current_mo.created_by
    updator_username = current_mo.latest_updator
    creator = None
    updator = None
    is_creator_found = False
    is_updator_found = False
    for admin in admin_list:
      if admin.username == creator_username:
        creator = admin
        is_creator_found = True
      if admin.username == updator_username:
        updator = admin
        is_updator_found = True
      if is_creator_found == True and is_updator_found == True:
        break

    # get currency unit table
    currency_unit_list = XCurrency.objects.order_by('object_id')

    # check null
    if name == "" or price == "" or currency_unit == "" or source == "" or category == "":
      # get image url
      mo_image_url = None
      if current_mo.image != "":
        mo_image_url = current_mo.image.url
        # mo_image_url += "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
      context = {
        'current_mo': current_mo,
        'currency_unit_list': currency_unit_list,
        'mo_image_url': mo_image_url,
        # creator
        'creator_hp_url': creator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
        'creator_username': creator_username,
        # updator
        'updator_hp_url': updator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
        'updator_username': updator_username,
        'error_message': "Critical fields can't be empty!"
      }
      return render(request, 'XMoneyRe/XUpdateMoneyObject.html', context)

    current_mo.name = name
    current_mo.price = price
    current_mo.source = source
    current_mo.currency_unit = currency_unit
    current_mo.category = category
    current_mo.trip_day = trip_day
    current_mo.local_date = local_date
    current_mo.description = description
    current_mo.latest_updator = latest_updator

    current_mo.save()

    return redirect('show_mo_spec', current_mo.object_id)

  else:

    # get curret user
    user = None
    if 'username' in request.COOKIES:
      username = request.COOKIES['username']
      try:
        user = XUserExInfo.objects.get(username=username)
      except:
        # not login or cookie error
        # redirect to login page
        return redirect('admin_login')
    else:
      return redirect('admin_login')

    # first view whole form
    current_mo = None
    try:
      current_mo = XMoneyObj.objects.get(object_id=mo_id)
    except:
      # not get
      return redirect('show_mo_spec', mo_id)

    # start update sequence
    # get admin_list
    admin_list = XUserExInfo.objects.order_by('username')
    creator_username = current_mo.created_by
    updator_username = current_mo.latest_updator
    creator = None
    updator = None
    is_creator_found = False
    is_updator_found = False
    for admin in admin_list:
      if admin.username == creator_username:
        creator = admin
        is_creator_found = True
      if admin.username == updator_username:
        updator = admin
        is_updator_found = True
      if is_creator_found == True and is_updator_found == True:
        break

    # get currency unit table
    currency_unit_list = XCurrency.objects.order_by('object_id')

    # get image url
    mo_image_url = None
    if current_mo.image != "":
      mo_image_url = current_mo.image.url
      # mo_image_url += "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    context = {
      'current_mo': current_mo,
      'mo_image_url': mo_image_url,
      'currency_unit_list': currency_unit_list,
      # creator
      'creator_hp_url': creator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
      'creator_username': creator_username,
      # updator
      'updator_hp_url': updator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
      'updator_username': updator_username,
      'error_message': ""
    }
    return render(request, 'XMoneyRe/XUpdateMoneyObject.html', context)


def updateMoneyObjectImage(request, mo_id):
  # not using
  # get curret user
  user = None
  if 'username' in request.COOKIES:
    username = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=username)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')

  # get current money object
  current_mo = None
  try:
    current_mo = XMoneyObj.objects.get(object_id=mo_id)
  except:
    # not get
    context = {
      'current_mo': None,
      'empty_message': "No record for id:" + mo_id + " object!"
    }
    return render(request, 'XMoneyRe/XMO-Spec.html', context)
  return redirect('new_moneyObject_image', current_mo.object_id)


def newMoneyObjectImage(request, mo_id):
  if request.method == 'POST':
    image_form = XMOImageForm(
      request.POST, request.FILES)
    if image_form.is_valid():
      image = image_form.cleaned_data['image']

      # get user
      user = None
      if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        try:
          user = XUserExInfo.objects.get(username=username)
        except:
          # not login or cookie error
          # redirect to login page
          return redirect('admin_login')
      else:
        return redirect('admin_login')

      # get current money object
      current_mo = None
      try:
        current_mo = XMoneyObj.objects.get(object_id=mo_id)
      except:
        # not get
        context = {
          'current_mo': None,
          'empty_message': "No record for id:" + mo_id + " object!"
        }
        return render(request, 'XMoneyRe/XMO-Spec.html', context)

      # check whether okay to process
      x_image = Image.open(image.file.name)
      width, height = x_image.size

      target_width = 1920
      target_heigbht = 1080

      if width < target_width or height < target_heigbht:
        # image not valid
        image_form = XMOImageForm()
        context={
          'current_mo': current_mo,
          'error_information': "size must bigger than 1920X1080",
          'image_form': image_form
        }
        return render(request, 'XMoneyRe/XUpdateMOImage.html', context)
      
      if current_mo.image != "":
        # delete and update previous tag
        # delete large version
        remove_imagebv_name = str(current_mo.object_id) + "-image-lv-" + current_mo.previous_tag

        try:
          os.remove(os.path.join(settings.MEDIA_ROOT +
                     settings.MEDIA_MO_IMAGE_PLACE, remove_imagebv_name))
        except:
          # delete not success
          image_form = XMOImageForm()
          context={
            'current_mo': current_mo,
            'error_information': "disk image-lv delete not success!",
            'image_form': image_form
          }
          return render(request, 'XMoneyRe/XUpdateMOImage.html', context)

        # delete small version
        remove_imagesv_name = str(current_mo.object_id) + "-image-sv-" + current_mo.previous_tag

        try:
          os.remove(os.path.join(settings.MEDIA_ROOT +
                     settings.MEDIA_MO_IMAGE_PLACE, remove_imagesv_name))
        except:
          # delete not success
          image_form = XMOImageForm()
          context={
            'current_mo': current_mo,
            'error_information': "disk image-sv delete not success!",
            'image_form': image_form
          }
          return render(request, 'XMoneyRe/XUpdateMOImage.html', context)

      # save new image
      # get postfix_name
      last_dot_position = image.name.rfind('.')
      picture_postfix_name = image.name[last_dot_position:]
      # get datetime as unique id
      unique_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
      # set new unique id
      current_mo.previous_tag = unique_id + picture_postfix_name
      # set current image name, just save lv to database
      image.name = str(current_mo.object_id) + "-image-lv-" + unique_id + picture_postfix_name
      # save to database and do pic copy
      current_mo.image = image
      current_mo.save()

      # process image lv and sv
      # deal with lv
      imagelv_name = str(current_mo.object_id) + "-image-lv-" + current_mo.previous_tag
      imagelv_path = os.path.join(settings.MEDIA_ROOT +
                      settings.MEDIA_MO_IMAGE_PLACE, imagelv_name)
      x_image_lv = Image.open(imagelv_path)
      width, height = x_image_lv.size
      target_width = 1920
      target_height = 1080
      # resize
      if width >= height:
        x_image_lv = x_image_lv.resize(
          (target_width, int(height/width*target_width)), Image.ANTIALIAS)
      else:
        x_image_lv = x_image_lv.resize(
        (int(width/height*target_height), target_height), Image.ANTIALIAS)
      width, height = x_image_lv.size
      # corp
      x = int((width - target_width)/2)
      y = int((height - target_height)/2)
      x_ending = x + target_width
      y_ending = y + target_height
      x_image_lv = x_image_lv.crop((x, y, x_ending, y_ending))
      x_image_lv.save(imagelv_path, format=x_image_lv.format, quality=100)
      # deal with sv
      target_width = 320
      target_height = 180
      x_image_lv.thumbnail((target_width, target_height))
      imagesv_name = str(current_mo.object_id) + "-image-sv-" + current_mo.previous_tag
      imagesv_path = os.path.join(settings.MEDIA_ROOT +
                      settings.MEDIA_MO_IMAGE_PLACE, imagesv_name)
      x_image_lv.save(imagesv_path, format=x_image_lv.format, quality=100)

      return redirect('show_mo_spec', current_mo.object_id)

  else:
    # new visit
    # get user
    user = None
    if 'username' in request.COOKIES:
      username = request.COOKIES['username']
      try:
        user = XUserExInfo.objects.get(username=username)
      except:
        # not login or cookie error
        # redirect to login page
        return redirect('admin_login')
    else:
      return redirect('admin_login')

    # get current money object
    current_mo = None
    try:
      current_mo = XMoneyObj.objects.get(object_id=mo_id)
    except:
      # not get
      context = {
        'current_mo': None,
        'empty_message': "No record for id:" + mo_id + " object!"
      }
      return render(request, 'XMoneyRe/XMO-Spec.html', context)

    image_form = XMOImageForm()
    context={
      'current_mo': current_mo,
      'error_information': "",
      'image_form': image_form
    }

    return render(request, 'XMoneyRe/XUpdateMOImage.html', context)


def deleteMO(request, mo_id):
  user = None
  if 'username' in request.COOKIES:
    username = request.COOKIES['username']
    try:
      user = XUserExInfo.objects.get(username=username)
    except:
      # not login or cookie error
      # redirect to login page
      return redirect('admin_login')
  else:
    return redirect('admin_login')

  # get current trip day
  # get trip day
  trip_info_object = XTripInfo.objects.order_by('object_id')[0]
  # tripday
  trip_day = trip_info_object.current_trip_day

  try:
    current_mo = XMoneyObj.objects.get(object_id=mo_id)
  except:
    return redirect('show_mo_spec', mo_id)

  # delete photos
  if current_mo.image != "":
    # delete and update previous tag
    # delete large version
    remove_imagebv_name = str(current_mo.object_id) + "-image-lv-" + current_mo.previous_tag

    try:
      os.remove(os.path.join(settings.MEDIA_ROOT +
                  settings.MEDIA_MO_IMAGE_PLACE, remove_imagebv_name))
    except:
      # delete not success
      image_form = XMOImageForm()
      context={
        'current_mo': current_mo,
        'error_information': "disk image-lv delete not success!",
        'image_form': image_form
      }
      return render(request, 'XMoneyRe/XUpdateMOImage.html', context)

    # delete small version
    remove_imagesv_name = str(current_mo.object_id) + "-image-sv-" + current_mo.previous_tag

    try:
      os.remove(os.path.join(settings.MEDIA_ROOT +
                  settings.MEDIA_MO_IMAGE_PLACE, remove_imagesv_name))
    except:
      # delete not success
      image_form = XMOImageForm()
      context={
        'current_mo': current_mo,
        'error_information': "disk image-sv delete not success!",
        'image_form': image_form
      }
      return render(request, 'XMoneyRe/XUpdateMOImage.html', context)


  current_mo.delete()

  return redirect('show_mo_tripday', trip_day)