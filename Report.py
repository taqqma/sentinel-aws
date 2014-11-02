#!/usr/bin/env /usr/local/bin/python2.7
# coding:utf-8

import os
import sys

def main():

    event_type = sys.argv[1]
    event_description = sys.argv[2]

    if event_type = '+failover-end':
        result = os.system(
            'cat <<EOF |'
            '/usr/sbin/sendmail -t To: 送信先メールアドレス\n'
            'From:  送信元メールアドレス\n'
            'Subject: Redis Notificatoin\n'
            '\n'
            'Event Type: '+ event_type + '\n'
            'Event Description '+ event_description + '\n'
            'Please check the redis status  \n'
            'EOF'
    )

if __name__ == "__main__":
    main()
