#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ftplib import FTP
import re
import os
import csv
import subprocess
import time
from datetime import datetime
import config as config
from SendEmail import SendEmail as semail


class GetFileFTP:

    @staticmethod
    def limpar_files():
        """Remove CSV and jpg files from system root folder."""
        r = re.compile(".*\.csv$|.*\.jpg$")
        all_file = os.listdir(config.path)
        files = filter(r.match, all_file)
        for f in files:
            print('Removendo {}'.format(f))
            os.remove(config.path + f)

    def get_list_file(self, host, port, user,
                      password, pasta, num_error):
        try:
            r = re.compile(".*\.jpg$")
            ftp = FTP()
            ftp.connect(host, port)
            ftp.login(user, password)
            ftp.cwd(pasta)
            all_files = ftp.nlst()
            files = filter(r.match, all_files)
            print('{}{}'.format(config.path, files[0][0:7]))
            name_file = '{folder}{file}.csv'.format(
                folder=config.path,
                file=files[0][0:7]
            )
            with open(name_file, 'wb') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(['namefile', 'data', 'time'])
                for f in files:
                    wr.writerow([
                        f,
                        f[8:18],
                        '{}:{}'.format(f[19:21], f[21:23])
                    ]
                    )
        except Exception as e:
            if num_error < config.numberAttempts:
                print('{} Tentativa rede {}'.format(
                    datetime.now(),
                    num_error
                ))
                print(e)
                time.sleep(config.waitingTime)
                self.get_list_file(
                    host,
                    port,
                    user,
                    password,
                    pasta,
                    num_error + 1
                )

    def main(self):
        # limpar_files()
        print('{} baixado dados'.format(datetime.now()))
        for ftpRota in config.ftpGetFiles:
            print('{} connect {}'.format(
                datetime.now(),
                ftpRota['port']
            ))
            self.get_list_file(
                ftpRota['host'],
                ftpRota['port'],
                ftpRota['user'],
                ftpRota['pass'],
                ftpRota['path'],
                0
            )
            pass

        print(str(datetime.now()) + " Gerando Grafico")
        subprocess.call(
            'Rscript {}creatPlot.R'.format(config.path),
            shell=True
        )
        print('send email')
        semail().main()
