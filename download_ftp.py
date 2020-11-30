import ftplib
import progressbar


ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
ftp.login()

def download(url, ftp, PATH_SAVE):
    '''url = 'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound_3D/01_conf_per_cmpd/SDF/00000001_00025000.sdf.gz'''
    segs = url.split('/')
    #print(segs)
    remote_path = '/'.join(segs[3:])
    fname = segs[-1]
    local_path = f'{PATH_SAVE}/{fname}'
    #print(remote_path)
    #print(local_path)
    size = ftp.size(remote_path)
    #print(size)
    size_MB = size/1024/1024
    #print(filename)
    widgets = [f'Downloading: {fname} {size_MB:.1f} MB', progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]

    pbar = progressbar.ProgressBar(widgets=widgets, maxval=size)
    #pbar.start()

    file = open(local_path, 'wb')
    def make_file_write(pbar, file):
        def file_write(data):
            nonlocal pbar
            file.write(data)
            pbar += len(data)
        return file_write

    file_write = make_file_write(pbar, file)
    ftp.retrbinary("RETR " + remote_path, file_write)


if __name__ == '__main__':
    #print(ftp)
    url = 'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound_3D/01_conf_per_cmpd/SDF/00025001_00050000.sdf.gz'
    PATH_SAVE = '/home/xcsc/dataset/pubchem/origin'
    download(url, ftp, PATH_SAVE)