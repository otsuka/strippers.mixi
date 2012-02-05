# vim:fileencoding=utf-8
from urllib import urlencode
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

USER_TIMELINE_URI    = '/2/voice/statuses/@me/user_timeline'
FRIENDS_TIMELINE_URI = '/2/voice/statuses/friends_timeline/%s'

def _get_user_timeline(self, count=20, start_index=0, since_id=None, trim_user=False, attach_photo=False):
    params = _build_params(count, start_index, since_id, trim_user, attach_photo)
    res = self.get(USER_TIMELINE_URI, params)
    return json.loads(res)

def _build_params(count, start_index, since_id, trim_user, attach_photo):
    if count > 200: count = 200
    elif count < 1: count = 1

    if start_index < 0: start_index = 0
    elif start_index > 199: start_index = 199

    params = {
            'count': count,
            'startIndex': start_index,
            }
    if trim_user:
        params['trim_user'] = 'true'
    if attach_photo:
        params['attach_photo'] = 'true'
    if since_id is not None:
        params['since_id'] = since_id
    return params

def _get_friends_timeline(self, group_id='', count=20, start_index=0, since_id=None, trim_user=False, attach_photo=False):
    params = _build_params(count, start_index, since_id, trim_user, attach_photo)
    uri = FRIENDS_TIMELINE_URI % str(group_id)
    res = self.get(uri, params)
    return json.loads(res)


API_METHODS = {
        'get_user_timeline'    : _get_user_timeline,
        'get_friends_timeline' : _get_friends_timeline,
        }
