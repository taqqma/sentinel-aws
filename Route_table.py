#!/usr/bin/env /usr/local/bin/python2.7
# coding: utf-8

import json
import os
from boto import ec2
from boto.vpc import VPCConnection
from Admin import Admin


logger = Admin()


def conn_route():
    """
    - boto経由でAWS-API接続し、Routingテーブル情報を取得
    - route_table.jsonにRouting-ID、VIPを設定しておくこと
    - aws_key.jsonにAWS鍵情報とリージョン情報を設定しておくこと
    """

    f = open(os.path.abspath(os.path.dirname(__file__))+'/config/aws_key.json', 'r')
    aws_config = json.load(f)
    aws_region = ec2.get_region(aws_config['region'])
    aws_id = aws_config['aws_access_key_id']
    aws_key = aws_config['aws_secret_access_key']
    f.close()

    f = open(os.path.abspath(os.path.dirname(__file__))+'/config/route_table.json', 'r')
    route_config = json.load(f)
    vpc_conn = VPCConnection(region=aws_region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
    ec2_conn = ec2.connect_to_region(region_name=aws_config['region'])
    route_id = vpc_conn.get_all_route_tables(route_config['route_table_id'])
    virtual_ip = route_config['vip']
    f.close()

    if not route_id:
        logger.logging("error", "route_id not found")

    return route_id, virtual_ip, vpc_conn, ec2_conn


class RouteTable:

    def create_route(self, master_node):
        """
        新master-IPを受け取って、VIPのDestinationを向け直すRouting-Tableを作りなおしている
        """

        vpc_conn = conn_route()[2]
        ec2_conn = conn_route()[3]
        route_table = conn_route()[0]
        vip = conn_route()[1]
        master_instance_id = ec2_conn.get_all_instances(filters={'private_ip_address': master_node})[0].instances[0].id

        if not master_instance_id:
            logger.logging("error", "master instance id not found")

        vpc_conn.create_route(route_table[0].id, vip, instance_id=master_instance_id)

    def delete_route(self):

        vpc_conn = conn_route()[2]
        vip = conn_route()[1]
        route_table = conn_route()[0]
        vpc_conn.delete_route(route_table[0].id, vip)
