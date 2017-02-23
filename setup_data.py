import os
import sys
import subprocess
import platform
import argparse
import time

import requests

def download(url, filepath, chunksize=100000, overwrite=False):
    if os.path.exists(filepath) and not overwrite:
        print('{} 파일이 존재합니다. 다운로드를 중단합니다.'.format(filepath))
        sys.exit(1)

    res = requests.get(url, stream=True)
    res.raise_for_status()

    file_size = int(res.headers.get('Content-Length'))
    print('다운로드 받을 파일 크기: {:.1f} MB'.format(file_size / 2**20))
    with open(filepath, 'wb') as target_file:
        total = 0
        for chunk in res.iter_content(chunksize):
            if chunk:
                target_file.write(chunk)
                total += len(chunk)
                print('{:.0%}'.format(total/file_size), end='\r')
                time.sleep(0.01)
        print('')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--format_dir', dest='format_dir', action='store_true', default=False)
    parser.add_argument(
        '--dirpath', dest='dirpath')
    args = parser.parse_args()

    # 사용자 경로 설정
    dirpath = '.' if not args.dirpath else args.dirpath
    if not os.path.exists(dirpath):
        print('오류! {} 경로가 존재하지 않습니다.'.format(os.path.abspath(dirpath)))
        return sys.exit(1)

    # 폴더 구성 설정
    if args.format_dir:
        # 사용자가 대상 경로를 지정하는 경우
        if args.dirpath:
            dirpath = args.dirpath
        # 사용자가 대상 경로를 지정하지 않는 경우
        else:
            environ_var = 'HOMEPATH' if platform.system() == 'Windows' else 'HOME'
            userhome = os.getenv(environ_var)
            dirpath = os.path.join(userhome, 'Documents')

        # create directory
        dirpath = os.path.join(dirpath, 'bigpy')
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            print('{} 경로 생성'.format(dirpath))

    print('경로: {}'.format(os.path.abspath(dirpath)))

    # 2. download data
    url = 'https://storage.googleapis.com/codebasic-website-159307.appspot.com/data/bigpy_data.zip'
    target = os.path.join(dirpath, 'data.zip')
    download(url, target)

    # 3. extract zip file
    # 압축 해제
    print('다운로드 받은 파일 압축 해제', end=' ... ')
    command_to_extract_zip = 'python -m zipfile -e {} {}'.format(target, dirpath)
    subprocess.run(command_to_extract_zip.split(), check=True)
    print('완료')

if __name__ == '__main__':
    main()
