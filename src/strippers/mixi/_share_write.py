# vim:fileencoding=utf-8
from strippers.mixi.graphapi import V_SELF, V_TOP_FRIENDS, V_FRIENDS, V_FRIENDS_OF_FRIENDS
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

SHARE_URI = '/2/share'

def _share(self, key, title, url, image=None, pc_url=None, smartphone_url=None, mobile_url=None, description=None, comment=None, privacy=V_FRIENDS):

    if privacy not in (V_FRIENDS_OF_FRIENDS, V_TOP_FRIENDS, V_FRIENDS, V_SELF):
        raise ValueError, 'The given privacy value is not supported. [' + privacy + ']'

    params = {
            'key'            : key,
            'title'          : title,
            'description'    : description,
            'primary_url'    : url,
            'comment'        : comment,
            'image'          : image,
            'pc_url'         : pc_url,
            'smartphone_url' : smartphone_url,
            'mobile_url'     : mobile_url,
            'privacy'        : { 'visibility' : privacy },
            }
    data = json.dumps(params)
    self.post(SHARE_URI, data, self.CONTENT_TYPE_JSON)
    

API_METHODS = { 'share' : _share, }
