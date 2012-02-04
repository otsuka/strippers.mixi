==============
strippers.mixi
==============

概要
====

`mixi Graph API`_ を Python から簡単に使えるようにするためのライブラリです。

.. _`mixi Graph API`: http://developer.mixi.co.jp/connect/mixi_graph_api/about_mixi_graph_api

インストール方法
================

easy_install を使ってインストールします。
依存ライブラリの `MultipartPostHandler`_ も自動的にインストールされます。

::

    # easy_install strippers.mixi


サポートしているAPI
===================

現在このライブラリがサポートしている mixi Graph API は以下の通りです。

`People API`_
-------------

READ_PROFILE (r_profile) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `友人一覧の取得`_
    - get_friends(group_id='`@friends`', sort_by=None, sort_order='ascending', count=20, start_index=0)
- 自分自身の取得
    - get_myself()

`Voice API`_
------------

READ_VOICE (r_voice) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `ユーザのつぶやき一覧の取得`_
    - get_user_timeline(count=20, start_index=0)
- `友人のつぶやき一覧の取得`_
    - get_friends_timeline(group_id='', count=20, start_index=0)

WRITE_VOICE (w_voice) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `つぶやきの投稿`_
    - update_status(status)
- `フォト付きつぶやきの投稿`_
    - update_status(status, photo)
- `つぶやきの削除`_
    - delete_status(status_id)

`Message API`_
--------------

READ_MESSAGE (r_message) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `受信メッセージ一覧の取得`_
    - get_messages(updated_since=None, count=50, start_index=0)
- `受信メッセージの取得`_
    - get_message(message_id)

WRITE_MESSAGE (w_message) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `メッセージの送信`_
    - send_message(recipient_id, title, body)
- `メッセージの閲覧状態の変更`_
    - change_message_status(message_id, read=True, replied=False)
- `メッセージの削除`_
    - delete_message(message_id)

`Check API`_
--------------

WRITE_SHARE (w_share) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `mixiチェックの投稿`_
    - share(key, title, url, image=None, pc_url=None, smartphone_url=None, mobile_url=None, description=None, comment=None, visibility=V_FRIENDS)


`Diary API`_
--------------

WRITE_DIARY (w_diary) スコープ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `画像無しの日記の投稿`_
    - write_diary(title, body, privacy=V_FRIENDS)


.. _`MultipartPostHandler`: http://pypi.python.org/pypi/MultipartPostHandler/0.1.0
.. _`People API`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/people-api
.. _`Voice API`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/voice-api
.. _`Message API`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/message-api
.. _`Check API`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/check-api
.. _`Diary API`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/diary-api
.. _`友人一覧の取得`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/people-api
.. _`ユーザのつぶやき一覧の取得`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/voice-api#toc-2
.. _`友人のつぶやき一覧の取得`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/voice-api#toc-3
.. _`つぶやきの投稿`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/voice-api#toc-9
.. _`フォト付きつぶやきの投稿`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/voice-api#toc-10
.. _`つぶやきの削除`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/voice-api#toc-11
.. _`受信メッセージ一覧の取得`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/message-api#toc-1
.. _`受信メッセージの取得`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/message-api#toc-1
.. _`メッセージの送信`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/message-api#toc-2
.. _`メッセージの閲覧状態の変更`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/message-api#toc-3
.. _`メッセージの削除`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/message-api#toc-4
.. _`mixiチェックの投稿`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/check-api
.. _`画像無しの日記の投稿`: http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/diary-api#toc-2


strippers.mixi モジュールの定数
===============================

スコープ
--------------

- READ_PROFILE
    - 'r_profile'
- READ_VOICE
    - 'r_voice'
- WRITE_VOICE
    - 'w_voice'
- READ_UPDATE
    - 'r_updates'
- WRITE_SHARE
    - 'w_share'
- READ_PHOTO
    - 'r_photo'
- WRITE_PHOTO
    - 'w_photo'
- READ_MESSAGE
    - 'r_message'
- WRITE_MESSAGE
    - 'w_message'
- WRITE_DIARY
    - 'w_diary'

公開設定
--------------

APIメソッドのprivacy、またはvisibility引数に渡す値。APIによってサポートされている公開設定の範囲は異なります。

- V_EVERYONE
    - 'everyone' : 全体に公開
- V_FRIENDS
    - 'friends' : 友人まで公開
- V_FRIENDS_OF_FRIENDS
    - 'friends_of_friends' : 友人の友人まで公開
- V_TOP_FRIENDS
    - 'top_friends' : 仲良しに公開
- V_SELF
    - 'self' : 非公開

特定のグループにのみへの公開('group')は、このライブラリでは今のところサポートされていません。




使用方法
==============

MixiGraphAPI オブジェクトの初期化
---------------------------------
::

    >>> from strippers.mixi import MixiGraphAPI, WRITE_VOICE, DEVICE_PC
    >>>
    >>> # mixi サービス登録情報を定義
    >>> consumer_key = 'xxxxxxxxxxxxxxxxxxxx'
    >>> consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    >>> redirect_uri = 'http://www.example.com/mixi/authorized'
    >>>
    >>> # 使用する API のスコープを指定
    >>> scopes = [WRITE_VOICE]
    >>>
    >>> # (1) MixiGraphAPI オブジェクトを生成
    >>> api = MixiGraphAPI(consumer_key, consumer_secret, scopes)
    >>>
    >>> # (2) ユーザ認可用 URL を取得
    >>> api.get_auth_url(device=DEVICE_PC)
    'https://mixi.jp/connect_authorize.pl?scope=w_voice&response_type=code&client_id=xxxxxxxxxxxxxxxxxxxx&display=pc'

    >>> # (3) 上の URL にアクセスして[同意する]と、サービス登録した redirect_uri に
    >>> # code パラメータ付きでリダイレクトされてきます。
    >>> # この code パラメータを利用します。
    >>> code = '5fbf8d9e55f0df0deff68cd4a8500701b3fe6baa'
    >>> 
    >>> # (4) MixiGraphAPI オブジェクトを初期化
    >>> api.initialize(code, redirect_uri)
    >>>
    >>> # 認可ユーザのアクセストークンとリフレッシュトークンを取得
    >>> access_token, refresh_token = api.tokens

MixiGraphAPI オブジェクトを初期化すると、各 API メソッドを実行できるようになります。

ユーザのアクセストークンとリフレッシュトークンが予め分かっている場合は、上記(1)～(4)の MixiGraphAPI オブジェクトの初期化処理は要らず、次のようにアクセストークンとリフレッシュトークンを引数に渡して MixiGraphAPI オブジェクトを生成するだけで済みます。

::

    >>> api = MixiGraphAPI(consumer_key, consumer_secret, scopes, access_token, refresh_token)

つぶやきの投稿
--------------
::

    >>> status = api.update_status('投稿なう')
    >>>
    >>> # 上のつぶやきを削除します
    >>> api.delete_status(status['id'])
    
フォト付きでつぶやきを投稿するには、画像ファイルのファイルパス、または「http(s)://」で始まる URL を第2引数に渡します。

::

    >>> api.update_status('フォト投稿なう', '/path/to/picture.jpg')
    >>>
    >>> # フォトだけの投稿も可能
    >>> api.update_status(photo='/path/to/picture.jpg')

トークンの有効期限切れ
----------------------

アクセストークン、リフレッシュトークンそれぞれに有効期限があります。アクセストークンの有効期限は約15分ですが、リフレッシュトークンが有効期限内は MixiGraphAPI オブジェクト内部で自動的に再取得(リフレッシュ)します。

リフレッシュトークンの有効期限は約6時間(ユーザ認可時に「常に同意する」のチェックを入れていれば約3ヶ月間)です。リフレッシュトークンが期限切れになった場合は、MixiGraphAPI オブジェクトの初期化処理が必要になります。つまり、再度ユーザ認可を行います。

::

    >>> from strippers.mixi import ExpiredTokenError
    >>>
    >>> try:
    >>>     api.update_status('リフレッシュトークン期限切れの場合')
    >>> except ExpiredTokenError:
    >>>     auth_url = api.get_auth_url(device=DEVICE_PC)
    >>>     # auth_url にアクセスしてユーザ認可処理...

