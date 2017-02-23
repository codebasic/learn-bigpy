import os
import sys
import subprocess
import requests

def download(url, filepath, chunksize=100000, overwrite=False):
    if os.path.exists(filepath) and not overwrite:
        print('{} 파일이 존재합니다. 다운로드를 중단합니다.'.format(filepath))
        sys.exit(1)

    res = requests.get(url)
    res.raise_for_status()

    file_size = int(res.headers.get('Content-Length'))
    print('다운로드 받을 파일 크기: {:1f} MB'.format(file_size / 2**20))
    with open(filepath, 'wb') as target_file:
        print('다운로드 진행 중 ...')
        for chunk in res.iter_content(chunksize):
            if chunk:
                target_file.write(chunk)
                #print('{:%}'.format(len(chunk)/file_size), end='\r')

def main():
    url = 'https://storage.googleapis.com/codebasic-website-159307.appspot.com/data/bigpy_data.zip'
    target = 'data.zip'

    # 1. download
    download(url, target)

    # 2. extract zip file
    # 압축 해제
    print('다운로드 받은 파일 압축 해제', end=' ... ')
    command_to_extract_zip = 'python -m zipfile -e {} .'.format(target).split()
    subprocess.run(command_to_extract_zip, check=True)
    print('완료')

if __name__ == '__main__':
    main()
