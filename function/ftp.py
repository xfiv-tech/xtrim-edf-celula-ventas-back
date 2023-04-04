import ftplib

def ftp_connect(host, user, passwd):
    ftp = ftplib.FTP(host)
    ftp.login(user, passwd)
    print(ftp.getwelcome())
    return ftp



def ftp_list(ftp, path):
    return ftp.nlst(path)


def ftp_mkdir(ftp, path):
    ftp.mkd(path)


def ftp_rmdir(ftp, path):
    ftp.rmd(path)

def ftp_upload(ftp, file, path):
    ftp.storbinary('STOR ' + path, file)


def ftp_download(ftp, path, file):
    ftp.retrbinary('RETR ' + path, file.write)


def ftp_close(ftp):
    ftp.quit()


