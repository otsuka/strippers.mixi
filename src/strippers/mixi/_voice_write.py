# vim:fileencoding=utf-8
from urllib import urlretrieve
import urllib2
import re
import os, os.path
from tempfile import mkstemp
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

STATUS_UPDATE_URI = '/2/voice/statuses/update'
STATUS_DELETE_URI = '/2/voice/statuses/destroy/%s'

_TMPFILE_PREFIX = 'strippers_mixi_voice_tmp'

def _update_status(self, status=None, photo=None):
    """つぶやきを投稿します。
    status、photo 引数のどちらか、または両方を指定します。
    photo には画像のファイルパス、または画像 URL を指定します。

    @param status: つぶやき本文
    @type status: str
    @param photo: 画像ファイルのパス、または画像ファイルの URL
    @type photo: str
    @raise TypeError: status、photo どちらのパラメータも指定されていない場合
    """
    if status and not photo: # つぶやきのみの投稿
        params = { 'status': status }
        res = self.post(STATUS_UPDATE_URI, params)
        return json.loads(res)
    elif photo: # フォトの投稿。つぶやきはなくてもOK
        photo_file, fd = _open_photo_file(photo)
        params = { 'photo': photo_file }
        if status:
            params['status'] = status
        try:
            res = self.post(STATUS_UPDATE_URI, params, self.CONTENT_TYPE_MULTIPART)
            return json.loads(res)
        finally:
            photo_file.close()
            if fd:
                # mkstemp() の一時ファイルは close() 処理を二度行う必要がある
                # http://ameblo.jp/icz-tech/entry-10195988170.html
                os.close(fd)
                # テンポラリファイルを削除
                os.unlink(photo_file.name)
    else:
        raise TypeError('status or photo argument is required.')

def _delete_status(self, id):
    """指定された ID のつぶやきを削除します。

    ID のつぶやきが存在しない場合は HTTPError (404 エラー) を送出します。

    @param id: 削除するつぶやきの ID
    @type id: str
    @raise HTTPError: 指定された ID のつぶやきが存在しない場合
    """
    self.delete(STATUS_DELETE_URI % str(id))


def _open_photo_file(path):
    """path が示すファイルの file オブジェクトとファイルディスクリプタを返します。

    path がシステム上のファイルを示す場合、ファイルディスクリプタは None です。

    path が URL だった場合、画像の URL とみなし、その画像を一時ファイルに保存します。
    そして、その一時ファイルの file オブジェクトとファイルディスクリプタを返します。
    """
    if re.match(r'^https?://.+', path):
        tmp = mkstemp(os.path.splitext(path)[1], _TMPFILE_PREFIX)
        urlretrieve(path, tmp[1])
        photo_file = open(tmp[1], 'rb')
        fd = tmp[0]
    else:
        fd = None
        photo_file = open(path, 'rb')
    return photo_file, fd


API_METHODS = {
        'update_status' : _update_status,
        'delete_status' : _delete_status,
        }
