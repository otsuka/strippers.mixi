# vim:fileencoding=utf-8
from urllib import urlencode
import types
import urllib2
import sys
import re
import logging
import MultipartPostHandler
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

log = logging.getLogger('graphapi')
#log_handler = logging.StreamHandler()
#log_handler.setLevel(logging.DEBUG)
#log.addHandler(log_handler)

__version__ = '1.0'


AUTORIZATION_URI = 'https://mixi.jp/connect_authorize.pl'
TOKEN_URI        = 'https://secure.mixi-platform.com/2/token'
API_HOST         = 'api.mixi-platform.com'

# デバイス定数の定義
DEVICE_PC         = 'pc'
DEVICE_SMARTPHONE = 'smartphone'
DEVICE_TOUCH      = 'touch'

# スコープ定数の定義
READ_PROFILE  = 'r_profile'
READ_VOICE    = 'r_voice'
WRITE_VOICE   = 'w_voice'
READ_UPDATES  = 'r_updates'
WRITE_SHARE   = 'w_share'
READ_PHOTO    = 'r_photo'
WRITE_PHOTO   = 'w_photo'
READ_MESSAGE  = 'r_message'
WRITE_MESSAGE = 'w_message'
WRITE_DIARY   = 'w_diary'

# 公開設定
V_EVERYONE           = 'everyone'
V_FRIENDS_OF_FRIENDS = 'friends_of_friends'
V_FRIENDS            = 'friends'
V_TOP_FRIENDS        = 'top_friends'
V_SELF               = 'self'

_api_mappings = {
    READ_VOICE    : 'strippers.mixi._voice_read',
    WRITE_VOICE   : 'strippers.mixi._voice_write',
    READ_PROFILE  : 'strippers.mixi._profile_read',
    READ_MESSAGE  : 'strippers.mixi._message_read',
    WRITE_MESSAGE : 'strippers.mixi._message_write',
    WRITE_SHARE   : 'strippers.mixi._share_write',
    WRITE_DIARY   : 'strippers.mixi._diary_write',
}

def set_api_module(scope, mod):
    _api_mappings[scope] = mod


class MixiGraphAPI(object):

    CONTENT_TYPE_MULTIPART = 'multipart/form-data'
    CONTENT_TYPE_JSON = 'application/json; charset=utf-8'

    def __init__(self, consumer_key, consumer_secret, scopes, access_token=None, refresh_token=None, use_https=True):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._use_https = bool(use_https)

        self.device = DEVICE_PC
        self.state = None
        self.auto_token_refresh = True
        self._token_updated = False

        self._access_token = access_token
        self._refresh_token = refresh_token
        self._expires = None
        self.scopes = tuple(scopes)
        if self._access_token and self._refresh_token and self.scopes:
            self._setup_apis()

    @property
    def tokens(self):
        """現在使われているアクセストークンとリフレッシュトークンのタプルを返します。

        """
        return self._access_token, self._refresh_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def token_updated(self):
        return self._token_updated

    def _setup_apis(self):
        for mod_name in [_api_mappings.get(scope) for scope in self.scopes if scope in _api_mappings]:
            if mod_name:
                # モジュールを動的にインポート
                __import__(mod_name)
                mod = sys.modules[mod_name]
                # MixiGraphAPI インスタンスに API メソッドをセット
                mappings = getattr(mod, 'API_METHODS')
                for name, func in mappings.items():
                    if not hasattr(self, name):
                        setattr(self, name, types.MethodType(func, self, MixiGraphAPI))

    def get_auth_url(self, device=None, state=None):
        if device:
            self.device = device
        if state:
            self.state = state
        params = {
                'client_id'     : self._consumer_key,
                'response_type' : 'code',
                'display'       : self.device,
                }
        if self.state:
            params['state'] = self.state
        params['scope'] = ' '.join(self.scopes)
        return AUTORIZATION_URI + '?' + urlencode(params)

    def initialize(self, auth_code, redirect_uri):
        params = {
                'grant_type'    : 'authorization_code',
                'client_id'     : self._consumer_key,
                'client_secret' : self._consumer_secret,
                'code'          : auth_code,
                'redirect_uri'  : redirect_uri
                }
        try:
            res = urllib2.urlopen(TOKEN_URI, urlencode(params)).read()
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise InvalidAuthCodeError('Auth code "%s" is invalid. (It maybe expired.)' % auth_code)
            else:
                raise
        tokens = json.loads(res)
        self._access_token = tokens['access_token']
        self._refresh_token = tokens['refresh_token']
        self._expires = tokens['expires_in']
        self._token_updated = True
        self._setup_apis()
        return self.tokens

    def _create_request(self, uri, http_method):
        if http_method not in ('GET', 'POST', 'DELETE', 'PUT'):
            raise TypeError('Invalid HTTP method.')

        class MethodCustomRequest(urllib2.Request):
            def get_method(self):
                return http_method

        return MethodCustomRequest(uri)

    def _build_request(self, uri, http_method=None):
        if http_method in (None, 'GET', 'POST'):
            req = urllib2.Request(uri)
        else:
            req = self._create_request(uri, http_method)
        req.add_header('Authorization', 'OAuth ' + self._access_token)
        return req

    def _parse_error(self, e):
        """API アクセスのエラーレスポンスから WWW-Authenticate ヘッダにセットされた情報を名前と値の dict 形式で返します。
        """
        headers = e.info()
        value = headers.getheader('WWW-Authenticate')
        if value:
            value = value[len('OAuth '):]
            value = re.sub(r'["\']', '', value)
            data = [ key_val.split('=') for key_val in value.split(',') ]
            return dict(data)
        return {}

    def _to_utf8(self, val):
        if isinstance(val, types.UnicodeType):
            return val.encode('utf-8')
        return val

    def _encode_params(self, params):
        """params に含まれるユニコード文字列を utf-8 に変換します。

        @param params: 対象の dict
        @type params: dict
        @rtype: dict
        """
        results = {}
        for key, val in params.items():
            results[self._to_utf8(key)] = self._to_utf8(val)
        return results

    def _build_api_uri(self, path):
        """
        指定されたパスが 'https://' または 'http://' で始まっていない場合、
        プロトコルと API ホストを加えた URI を返します。
        'https://'、'http://' で始まっている場合は、何もせずにそのまま返します。
        
        @param path: パス
        @type path: str
        @return: URI
        @rtype: str
        """
        if not path.startswith('https://') and not path.startswith('http://'):
            protocol = 'https://' if self._use_https else 'http://'
            if not path.startswith('/'):
                path = '/' + path
            return protocol + API_HOST + path
        else:
            return path

    def post(self, uri, params=None, content_type=None):
        return self._send_api_request(uri, params, 'POST', content_type)

    def get(self, uri, params=None):
        return self._send_api_request(uri, params, 'GET')

    def put(self, uri, params=None, content_type=None):
        return self._send_api_request(uri, params, 'PUT', content_type)

    def delete(self, uri, params=None):
        return self._send_api_request(uri, params, 'DELETE')

    def _send_api_request(self, uri, params=None, http_method='GET', content_type=None, try_count=1):
        """
        @param uri: リクエスト URI
        @type uri: str
        @param params: リクエストパラメータ。
        @type params: dict または str
        @param http_method: リクエストの HTTP メソッドを示す文字列。'GET'、'POST'、'DELETE'。デフォルトは 'GET'
        @type http_method: str
        @param content_type: Content-Type
        @type content_type: str
        """
        if params is None:
            data = ''
        elif isinstance(params, types.DictType):
            # MultipartPostHandler は urlencode() を勝手にやってくれるので、
            # multipart 引数が指定されている場合は urlencode() しない。
            params = self._encode_params(params)
            data = params if content_type == self.CONTENT_TYPE_MULTIPART else urlencode(params)
        else:
            data = str(self._to_utf8(params))

        uri = self._build_api_uri(uri)

        http_method = http_method.upper()
        if http_method in ('POST', 'PUT'):
            req = self._build_request(uri, http_method)
            req.add_data(data)
        else: # GET or DELETE
            req = self._build_request(uri + '?' + data, http_method)

        if content_type is not None:
            if content_type == self.CONTENT_TYPE_MULTIPART:
                opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
            else:
                opener = urllib2.build_opener()
                req.add_header('Content-Type', content_type)
        else:
            opener = urllib2.build_opener()

        log.debug(u"Sent an api request: %s", req.get_full_url())
        try:
            return opener.open(req).read()
        except urllib2.HTTPError, e:
            if 400 <= e.code < 500:
                error_info = self._parse_error(e)
                error_msg = error_info.get('error')
                if error_msg == 'expired_token': # アクセストークンの有効期限切れ
                    if self.auto_token_refresh and try_count <= 1: # 念のため無限ループになるのを抑止
                        # アクセストークンを再発行して、再度 API リクエストを送信
                        self.reissue_token()
                        return self._send_api_request(uri, params, http_method, content_type, try_count + 1)
                    raise ExpiredTokenError('Access token is expired.')
                elif error_msg == 'insufficient_scope': # アクセスに必要なスコープが認可されていない
                    raise InsufficientScopeError(error_info.get('scope'))
                elif error_msg == 'invalid_request': # 不正なリクエスト内容
                    raise InvalidRequestError()
                elif error_msg == 'invalid_token': # 不正なアクセストークン
                    raise InvalidTokenError()
                else: # その他
                    raise
            else:
                raise

    def reissue_token(self):
        """アクセストークンを再発行します。
        リフレッシュトークンが有効期限切れの場合、再発行は失敗し、ExpiredTokenError を送出します。
        """
        params = {
                'grant_type'    : 'refresh_token',
                'client_id'     : self._consumer_key,
                'client_secret' : self._consumer_secret,
                'refresh_token' : self._refresh_token
                }
        try:
            res = urllib2.urlopen(TOKEN_URI, urlencode(params)).read()
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise ExpiredTokenError('Refresh token is expired.', self.get_auth_url())
            else:
                raise
        tokens = json.loads(res)
        self._access_token = tokens['access_token']
        self._refresh_token = tokens['refresh_token']
        self._expires = tokens['expires_in']
        self._token_updated = True


class MixiGraphAPIError(Exception):
    pass


class InvalidAuthCodeError(MixiGraphAPIError):
    pass


class InvalidRequestError(MixiGraphAPIError):
    pass


class InsufficientScopeError(MixiGraphAPIError):

    def __init__(self, scope):
        self.scope = scope

    def __str__(self):
        return self.scope


class InvalidTokenError(MixiGraphAPIError):

    def __init__(self, message):
        super(InvalidTokenError, self).__init__(message)


class ExpiredTokenError(InvalidTokenError):

    def __init__(self, message, auth_url=None):
        super(ExpiredTokenError, self).__init__(message)
        self.auth_url = auth_url

