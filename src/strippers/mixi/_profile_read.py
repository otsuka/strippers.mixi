# vim:fileencoding=utf-8
from urllib import urlencode
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

PEOPLE_URI = '/2/people/@me/%s'

def _get_friends(self, group_id='@friends', sort_by=None, sort_order='ascending', thumbnail_privacy='everyone', count=20, start_index=0):
    """
    @param sort_by "displayName" が指定可能。指定がない場合はid順
    @type sort_by str
    @param thumbnail_privacy "everyone" or "friends"
    @type thumbnail_privacy str
    """
    params = {
            'count': count,
            'startIndex': start_index,
            'sortOrder': sort_order,
            'thumbnailPrivacy': thumbnail_privacy,
            }
    if sort_by:
        params['sortBy'] = sort_by
    uri = PEOPLE_URI % str(group_id)
    res = self.get(uri, params)
    return json.loads(res)

def _get_myself(self):
    return _get_friends(self, '@self', count=1)


API_METHODS = {
        'get_friends' : _get_friends,
        'get_myself' : _get_myself,
        }
