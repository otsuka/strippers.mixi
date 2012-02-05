# vim:fileencoding=utf-8
import urllib2
from strippers.mixi.graphapi import V_SELF, V_TOP_FRIENDS, V_FRIENDS, V_FRIENDS_OF_FRIENDS, V_EVERYONE
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

DIARY_URI = '/2/diary/articles/@me/@self'

def _write_diary(self, title, body, privacy=V_FRIENDS):
    """
    画像無しで日記を投稿します。
    文字数制限はこのメソッドではチェックしません。そのままAPIに送信されます。

    @param title: 日記のタイトル (全角100文字以内)
    @type title: str
    @param body: 日記の本文 (全角10,000文字以内)
    @type body: str
    @param privacy: 日記の公開範囲
    @type privacy: str
    @return: 'id' キーを持つ dict オブジェクト
    @rtype: dict
    """
    if privacy not in (V_EVERYONE, V_FRIENDS_OF_FRIENDS, V_TOP_FRIENDS, V_FRIENDS, V_SELF):
        raise ValueError, 'The given privacy value is not supported. [' + privacy + ']'

    params = {
            'title'  : title,
            'body'   : body,
            'privacy': {'visibility': privacy},
            }
    data = json.dumps(params)
    try:
        res = self.post(DIARY_URI, data, self.CONTENT_TYPE_JSON)
        return json.loads(res)
    except urllib2.HTTPError, e:
        if e.code == 400: # 文字数制限オーバー
            error = json.loads(e.read())
            raise OverflowError, error['error_description']
        else:
            raise

API_METHODS = {
        'write_diary' : _write_diary,
        }
