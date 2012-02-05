# vim:fileencoding=utf-8
import urllib2
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

MESSAGE_SEND_URI = '/2/messages/@me/@self/@outbox'
MESSAGE_URI      = '/2/messages/@me/@self/@inbox/%s'

def _send_message(self, recipient_id, title, body):
    """
    メッセージを送信します。

    @param recipient_id: 宛先ユーザの ID
    @type recipient_id: str
    @param title: 件名
    @type title: str
    @param body: 本文
    @type body: str
    @return: 'id' キーを持つ dict オブジェクト
    @rtype: dict
    """
    params = {
            'title'      : title,
            'body'       : body,
            'recipients' : [recipient_id],
            }
    data = json.dumps(params)
    res = self.post(MESSAGE_SEND_URI, data, self.CONTENT_TYPE_JSON)
    return json.loads(res)

def _delete_message(self, message_id):
    uri = MESSAGE_URI % str(message_id)
    try:
        res = self.delete(uri)
        return True
    except urllib2.HTTPError, e:
        if e.code == 404:
            return True
        else:
            raise

def _change_message_status(self, message_id, read=True, replied=False):
    uri = MESSAGE_URI % str(message_id)
    if replied:
        params = { 'status': 'replied' }
    elif read:
        params = { 'status': 'read' }
    else:
        return
    data = json.dumps(params)
    res = self.put(uri, data, self.CONTENT_TYPE_JSON)
    return json.loads(res)


API_METHODS = {
        'send_message'          : _send_message,
        'delete_message'        : _delete_message,
        'change_message_status' : _change_message_status,
        }
