# Hatebu::Tracker #

## Hatebu::Trackerとは ##

はてなWebHookの「お気に入り」ユーザによるブックマーク通知を受け取り、Notify.io へ中継するWebサービスです。 このサービスの利用者は、Notify.io の通知ルーティングサービスを利用して、はてなWebHookの通知を（おそらく）ほぼリアルタイムにデスクトップで受信することができます。

また、それらの通知は Notify.io が提供するアウトレット（Outlet）を追加することで、iPhone や Jabberクライアント、email クラアント で受信することもできます。 

## 関連エントリー ##

* [GAEではてブのお気に入りユーザーが今何をブクマしているのかリアルタイムに追跡するためのサービス作ってみた - 今日もスミマセン。](http://d.hatena.ne.jp/snaka72/20091227/1261887975)
* [Notify.ioからの通知をリアルタイムに受け取るクラアント作った（Windows版） - 今日もスミマセン。](http://d.hatena.ne.jp/snaka72/20091231/1262284621)

## GAEへのデプロイ方法 ##

+ ソース一式を git clone/zip downlod などで入手します
+ アプリケーションのルートディレクトリにある secret.yaml を開き
+ apikey: の (put your notify.io api key here) を 自分の Notify.io APIKey に置き換えます。
+ app_config.py などで、GAEにデプロイするとサービスとして稼働します。

## LICENSE ##

Copyright (c) 2010 snaka
[The MIT License](http://creativecommons.org/licenses/MIT/deed.ja)


