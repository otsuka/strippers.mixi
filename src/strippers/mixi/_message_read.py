# vim:fileencoding=utf-8
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

MESSAGE_URI = '/2/messages/@me/@inbox/%s'

def _get_messages(self, updated_since=None, count=50, start_index=0):
    """
    認可ユーザが受信したメッセージ一覧を取得します。

    @param updated_since: このパラメータにて指定された日時よりも新しいメッセージを、APIの取得結果として返却します。文字列で指定する場合、日時の書式は「yyyy-mm-ddThh:mm:ssZ」や「yyyy-mm-ddThh:mm:ss+09:00」とします
    @type updated_since: str

    @todo: update_since パラメーターを datetime オブジェクトでも指定できるようにする
    """
    params = {
            'count': count,
            'startIndex': start_index,
            'fields': '@all',
            }
    if updated_since:
        # TODO: datetime オブジェクトでも指定できるようにする
        params['updatedSince'] = updatedSince
    uri = MESSAGE_URI % ''
    res = self.get(uri, params)
    return json.loads(res)

def _get_message(self, message_id):
    """
    認可ユーザが受信した指定された ID のメッセージを取得します。

    @param message_id: 取得するメッセージの ID
    @type message_id: str
    @rtype: dict
    """
    uri = MESSAGE_URI % str(message_id)
    res = self.get(uri, params)
    return json.loads(res)


API_METHODS = {
        'get_message'  : _get_message,
        'get_messages' : _get_messages,
        }
