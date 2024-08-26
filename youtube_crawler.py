from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

# ChromeDriver 경로 설정
driver_path = 'C:/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(driver_path)

# 엑셀 파일에서 유튜브 채널 URL 읽기
df = pd.read_excel('youtube_channels.xlsx')

# 각 유튜브 채널의 커뮤니티 탭 크롤링
job_posts = []

for index, row in df.iterrows():
    channel_url = row['channel_url']  # 엑셀에서 채널 URL 읽기ㅊ ㅋㅌ
    driver.get(channel_url)

    # 페이지 로드 대기
    time.sleep(random.uniform(5, 10))

    # BeautifulSoup으로 페이지 소스 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 1. 채널 이름 가져오기
    channel_name_element = soup.find('span', {'class': 'yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap'})
    channel_name = channel_name_element.get_text(strip=True) if channel_name_element else 'Unknown'

    # 2. 게시글의 날짜 가져오기
    date_element = soup.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'})
    post_date = date_element.get_text(strip=True) if date_element else 'Unknown'

    # 3. '편집자', '썸네일러', '구인' 키워드를 포함한 게시물 찾기
    posts = soup.select('yt-formatted-string#content-text')
    for post in posts:
        content = post.get_text()
        if any(keyword in content for keyword in ['편집자', '썸네일러', '구인', '급여']):
            # 결과 저장
            job_posts.append({'channel_name': channel_name, 'post_date': post_date, 'content': content})

    # 유튜브 크롤링 후 대기 시간 추가
    time.sleep(random.uniform(15, 25))

# 수집한 게시물을 엑셀 파일로 저장
job_posts_df = pd.DataFrame(job_posts)
job_posts_df.to_excel('filtered_job_posts.xlsx', index=False)

# 드라이버 종료
driver.quit()
