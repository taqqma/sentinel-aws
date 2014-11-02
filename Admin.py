#!/usr/bin/env /usr/local/bin/python2.7
# coding: utf-8

import os
import logging


class Admin:


    def error_report(self, subject,error):
        result = os.system(
            'cat <<EOF | '
            '/usr/sbin/sendmail -t To: yoshida@poppin-games.com\n'
            'From: dsky-infra@poppin-games.com\n'
            'Subject: ' + subject + '\n'
            '\n'
            + error + '\n'
            'EOF'
        )


    def logging(self, log_type,message):
        logging.basicConfig(level=logging.DEBUG,format="%(asctime)s- %(name)s - %(levelname)s - %(message)s")

        if log_type == "info":
            logging.info(message)
        elif log_type == "error":
            logging.error(message)
        else:
            logging.error(message)