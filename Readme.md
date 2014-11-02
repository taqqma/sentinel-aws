Sentinel-AWS
===========================
Redis-SentinelをAWS-VPC環境で動作させた時に
Routing-VIPを新masterに向け直すスクリプト

使い方
--------
    /etc/sentinel.conf

    daemonize yes
    port 26379
    pidfile "/var/run/redis_sentinel.pid"
    loglevel notice
    logfile "/var/log/redis_sentinel.log"
    sentinel monitor mymaster 192.168.240.171 6379 1
    sentinel down-after-milliseconds mymaster 30000
    sentinel parallel-syncs mymaster 2
    sentinel can-failover mymaster yes
    sentinel failover-timeout mymaster 900000
    sentinel notification-script mymaster /root/sentinel-aws/Report.py
    sentinel client-reconfig-script mymaster /root/sentinel-aws/Sentinel-aws.py

前提条件
--------
1. rootユーザで各Redisインスタンスがパス無し鍵認証接続できること
2. 各RedisインスタンスのENIについて、Source/Desc ChechがOFFになっていること
3. 各Redisインスタンスが所属するRoutingテーブルにvipを設定し、masterのRedisのENIにDestinationを向けること
4. botoがインストールされていること
5. redis2.6系であること（redis2.8系は動かない）

設定ファイル
------
- config/aws_key.json : AWSアクセスキー, AWSシークレットキー, リージョンを指定
- config/route_table.json : VPCのRoutingテーブルのid, vip, Routingテーブル名
- Report.py : レポートメールの送信元/送信先メールアドレス

フェイルオーバーの流れ
--------
1. Sentinelがmaster死亡を検知
2. Sentinelが新masterを選出、レプリケーション再構築
3. Sentinelによって Sentinel-aws.pyがキックされる。キックされるタイミングは3フェーズ

    3-1.  Failover started (a slave is already promoted)
    3-2.  Failover finished (all the additional slaves already reconfigured)
    3-3.  Failover aborted (in that case the script was previously called when the failover started, and now gets called again with swapped addresses).

    ★Sentinel-aws.pyは3-2だけで発動する
渡される引数 :
   (master-name) (role) (state) (from-ip) (from-port) (to-ip) (to-port)
   ★ state : 3-2の時、endが渡される

4. 3によって旧masterに紐付いていたVIPは、新masterに紐付け直される
5. Report.pyによって、フェイルオーバーの完了をメールで通知

参照
--------
<>
