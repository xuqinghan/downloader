import gevent
from gevent import monkey
# this needs to be AFTER python imports, but BEFORE package imports
monkey.patch_all()
import pubchem
import argparse

parser = argparse.ArgumentParser(description='帮助描述信息', prog='下载器',
                                 usage="python pubchem_downloader.py 'D:/chem/g/test_batch' 'D:/chem/g/urls.txt'", epilog='底部显示信息')  # 括号里面可以什么都不写，会走默认
parser.add_argument('PATH_SAVE', type=str, help='path to save')
parser.add_argument('fname_urls_txt', type=str, help='[name].fname_urls_txt')



def download(urls, PATH_SAVE):
    tasks = [gevent.spawn(pubchem.download, url, PATH_SAVE) for url in urls]
    gevent.joinall(tasks)
    print('Tasks done!')


def test():
    urls = ['ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound_3D/01_conf_per_cmpd/SDF/00025001_00050000.sdf.gz',
            'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound_3D/01_conf_per_cmpd/SDF/00050001_00075000.sdf.gz',
            ]

    PATH_SAVE = '/home/xcsc/dataset/pubchem/origin'
    download(urls, PATH_SAVE)

def load_urls(fname_urls_txt):
    urls = open(fname_urls_txt, 'r').readlines()
    #去掉空格
    urls = [url.strip() for url in urls]
    #去掉空行
    urls = [url for url in urls if url != '']
    return urls

if __name__ == '__main__':
    args = parser.parse_args()  # 命令行参数解析后存放的位置
    PATH_SAVE = args.PATH_SAVE
    fname_urls_txt = args.fname_urls_txt
    #fname_urls_txt = './tests/urls.txt'
    urls = load_urls(fname_urls_txt)
    print(urls)
    download(urls, PATH_SAVE)