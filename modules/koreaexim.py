import pandas as pd

def 엑셀읽기(파일경로):
    프레임 = pd.read_excel(파일경로, skiprows=3, parse_cols="C:K", header=None)
    프레임 = 프레임.dropna(how='all')
    프레임 = 프레임.reset_index(drop=True)
    return 프레임

def 표정보추출(프레임):
    색인시작목록 = list(프레임[프레임.notnull().sum(1) == 1].index)
    색인종료목록 = 색인시작목록[1:]
    색인종료목록.append(len(프레임))
    제목목록 = [프레임.ix[i, 0].lower() for i in 색인시작목록]
    return list(zip(제목목록, 색인시작목록, 색인종료목록))

def 데이터프레임추출(파일경로):
    프레임 = 엑셀읽기(파일경로)
    표정보목록 = 표정보추출(프레임)

    표사전 = {}
    for 표정보 in 표정보목록:
        제목, 시작, 종료 = 표정보
        # 표 길이가 1줄 이하면 제외
        if 종료 - 시작 < 2: continue
        표 = 프레임.iloc[시작:종료]
        # 열제목 설정
        열제목 = 표.iloc[1, 1:]
        열제목.name = None
        표 = 표.iloc[2:]
        표 = 표.set_index(0)
        표.columns = 열제목
        표.index.name = 제목.upper()
        # NaN 색인 제거
        표 = 표[pd.notnull(표.index)]
        표사전[제목] = 표

    return 표사전
