#!/usr/bin/env /usr/local/bin/python2.7
# coding: utf-8

import sys
import subprocess
from Route_table import RouteTable
from Admin import Admin


logger = Admin()


def main():
    """
    - Sentinel側から、Statusオプションを渡される（endで発動）
    - 既にSentinel側でｍaster昇格しているので、infoで新master-IPを取得
    - 新Routing-Tableを作成
    """

    m = RouteTable()

    sentinel_name = sys.argv[1]
    sentinel_role = sys.argv[2]
    sentinel_status = sys.argv[3]
    sentinel_srcip = sys.argv[4]
    sentinel_srcport = sys.argv[5]
    sentinel_toip = sys.argv[6]
    sentinel_toport = sys.argv[7]

    if sentinel_status == 'end':
        m.delete_route()
        master_ips = subprocess.check_output(
            "redis-cli -p 26379 info | grep master0 | cut -d '=' -f 4 | cut -d ':' -f 1", shell=True
        )
        master_ip = master_ips.rstrip()
        if master_ip == 0:
            logger.logging("error", "could not get master ip from sentinel")
        else:
            m.create_route(master_ip)
            logger.logging("info", "create new routing table")

if __name__ == "__main__":
    main()