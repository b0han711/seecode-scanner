# coding: utf-8
import os

from ftplib import FTP


class FTPWork(object):

    def __init__(self, host='127.0.0.1', port=21, username=None, password='', debug=True):
        self.ftp = FTP()
        self.ftp.connect(host=host, port=port, timeout=10)
        if not username:
            self.ftp.login()
        else:
            self.ftp.login(user=username, passwd=password)
        self.debug = debug
        self.ftp.debugging = self.debug
        self.ftp.getwelcome()

    def __del__(self):
        self.ftp.close()

    def debug_print(self, message):
        """

        :param message:
        :return:
        """
        if self.debug:
            print(message)

    def check_dir_exists(self, path):
        """
        检测路径是否存在
        :param path:
        :return:
        """
        try:
            result = False
            resp = self.ftp.voidcmd('CWD {0}'.format(path))
            if resp and '250' in resp:
                result = True
            return result
        except Exception as ex:
            return False

    def make_dir(self, ftp_path):
        """
        创建目录
        :param ftp_path:
        :return:
        """
        result = False
        try:
            status = self.check_dir_exists(path=ftp_path)
            if not status:
                resp = self.ftp.mkd(ftp_path)
                if resp:
                    result = True
        except OSError as ex:
            pass
        return result

    def remove_dir(self, ftp_path):
        """
        移除目录
        :param ftp_path:
        :return:
        """
        result = False
        try:
            status = self.check_dir_exists(path=ftp_path)
            if status:
                resp = self.ftp.rmd(ftp_path)
                if resp:
                    result = True

        except OSError as ex:
            pass
        return result

    def upload_file(self, local_file, remote_file):
        """
        上传文件
        :param local_file:  本地文件
        :param remote_file: 远程文件
        :return:
        """
        result = False
        try:
            if os.path.isfile(local_file):
                with open(local_file, 'rb') as fp:
                    resp = self.ftp.storbinary('STOR {0}'.format(remote_file), fp)
                    if resp and '226' in resp:
                        result = True
                    return result
            else:
                raise FileNotFoundError('"{0}"文件不存在。'.format(local_file))
        except FileNotFoundError as ex:
            pass
        return result

    def delete_file(self, ftp_path):
        """
        删除文件
        :param ftp_path:
        :return:
        """
        result = False
        try:
            f_list = self.ftp.nlst(ftp_path)
            for i in f_list:
                self.ftp.delete(i)
                result = True
        except FileNotFoundError as ex:
            pass
        return result

    def is_same_size(self, local_file, remote_file):
        """
        判断远程文件和本地文件大小是否一致

        :param local_file:  本地文件
        :param remote_file: 远程文件
        :return:
        """
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as ex:
            remote_file_size = -1

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as ex:
            local_file_size = -1

        self.debug_print('local_file_size:{0}, remote_file_size:{1}'.format(local_file_size, remote_file_size))
        if remote_file_size == local_file_size:
            return True
        else:
            return False

    def download_file(self, local_file, remote_file):
        """
        下载文件
        :param local_file:  本地文件
        :param remote_file: 远程文件
        :return:
        """
        self.debug_print("download_file()---> local_path = {0}, remote_path = {1}".format(local_file, remote_file))

        if self.is_same_size(local_file, remote_file):
            self.debug_print('{0} 文件大小相同，无需下载'.format(local_file))
            return False
        else:
            try:
                self.debug_print('>>>>>>>>>>>>下载文件到: {0} ... ...'.format(local_file))
                buf_size = 1024
                with open(local_file, 'wb') as file_handler:
                    self.ftp.retrbinary('RETR {0}'.format(remote_file), file_handler.write, buf_size)
                return True
            except Exception as ex:
                self.debug_print('下载文件出错，出现异常：{0} '.format(ex))
                return False

    def close(self):
        self.ftp.close()


if __name__ == '__main__':
    ff = FTPWork(host='10.168.6.26', username='ftp', password='ftp123')
    status = ff.make_dir('/seecode/group/app5')
    status = ff.check_dir_exists('/seecode/group/app4')
    print(ff.upload_file('/etc/php.ini.default','/seecode/group/app5/php.ini.default'))

    #ff.download_file("G:/ftp_test/XTCLauncher.apk", "/App/AutoUpload/ouyangpeng/I12/Release/XTCLauncher.apk")
    ff.download_file("/tmp/ftp/php.ini", "/seecode/group/app5/php.ini.default")

