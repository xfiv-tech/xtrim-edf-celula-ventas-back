import ftplib

def ftp_connect(host, user, passwd):
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, passwd)
        print("Conecion Ftp: ",ftp.getwelcome())
        return ftp
    except Exception as e:
        print(e)
        return None



def ftp_list(ftp, path):
    try:
        return ftp.nlst(path)
    except Exception as e:
        print(e)
        return None


def ftp_mkdir(ftp, path):
    ftp.mkd(path)


def ftp_rmdir(ftp, path):
    ftp.rmd(path)

def ftp_upload(ftp, file):
    ftp.storbinary('STOR ' + file)


def ftp_download(ftp, path, file):
    ftp.retrbinary('RETR ' + path, file.write)


def ftp_close(ftp):
    ftp.quit()


