import json
from django import template

register = template.Library()

@register.simple_tag
def profile_get(profile, key):
    json_dict = json.loads(profile.options)
    return json_dict.get(key,"")