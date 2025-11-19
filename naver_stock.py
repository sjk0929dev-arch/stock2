import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Stock API")

def get_stock_info(keyword):
    # 1) 네이버 주식 검색 → 종목코드 찾기
    search_url = f"https://m.stock.naver.com/search?keyword={keyword}"
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # 모바일 버전은 데이터가 span 등에 숨어 있음
    code_tag = soup.select_one("a.stock_item")
    if not code_tag:
        return {"error": "종목을 찾을 수 없음"}

    code = code_tag.get("href").split("/")[-1]

    # 2) 기업 개요 페이지 수집
    info_url = f"https://finance.naver.com/item/main.nhn?code={code}"
    r2 = requests.get(info_url)
    soup2 = BeautifulSoup(r2.text, "html.parser")

    # 예: 현재가, PER 등 파싱
    today = soup2.select_one("p.no_today span.blind").text
    per = soup2.select_one("table tbody tr td span.blind").text

    return {
        "name": keyword,
        "code": code,
        "price": today,
        "per": per,
        "link": info_url,
    }


# Streamlit API 엔드포인트
keyword = st.query_params.get("q", None)

if keyword:
    st.json(get_stock_info(keyword))
else:
    st.write("Use /?q=삼성전자 형태로 호출하세요.")
