from django import template

from datetime import datetime

register = template.Library()

@register.inclusion_tag('XMoneyRe/XMoneyObj-SingleOverview.html')
def show_single_overview(x_money_object, admin_list):
  # creator_hp_url, , updator_hp_url, 
  creator_username = x_money_object.created_by
  updator_username = x_money_object.latest_updator
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
  # name
  name = x_money_object.name
  if len(name) > 10:
    name = name[:10] + "..."
  # des
  description = x_money_object.description
  if len(description) > 10:
    description = description[:10] + "..."


  # get image url
  mo_image_url = None
  if x_money_object.image != "":
    mo_image_url = x_money_object.image.url
    mo_image_url = mo_image_url.replace("lv", "sv")
    # mo_image_url += "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  return {
    'x_money_object': x_money_object,
    'mo_image_url': mo_image_url,
    'name': name,
    'description': description,
    # creator
    'creator_hp_url': creator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    'creator_username': creator_username,
    # updator
    'updator_hp_url': updator.headportrait.url + "?rnd=" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    'updator_username': updator_username
  }