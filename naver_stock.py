import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Stock API")

def get_stock_code(query):
    """
    네이버 모바일 검색에서 종목코드 가져오기
    """
    url = f"https://m.search.naver.com/search.naver?query={query}+주가"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    # meta 태그에 naverfinance:code가 있음
    meta = soup.find("meta", {"property": "naverfinance:code"})
    if meta and meta.get("content"):
        return meta["content"]
    return None

def get_stock_info(keyword):
    # 1) 종목코드 가져오기
    code = get_stock_code(keyword)
    if not code:
        return {"error": "종목을 찾을 수 없음"}

    # 2) 기업 개요 페이지 수집
    info_url = f"https://finance.naver.com/item/main.nhn?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r2 = requests.get(info_url, headers=headers)
    soup2 = BeautifulSoup(r2.text, "lxml")

    # 예: 현재가, PER 등 파싱
    today_tag = soup2.select_one("p.no_today span.blind")
    today = today_tag.text.strip() if today_tag else "N/A"

    per_tag = soup2.select_one("table tbody tr td span.blind")
    per = per_tag.text.strip() if per_tag else "N/A"

    return {
        "name": keyword,
        "code": code,
        "price": today,
        "per": per,
        "link": info_url,
    }

# Streamlit API 엔드포인트
keyword = st.query_params.get("q", "")
keyword = keyword.strip()  # 공백 제거

if keyword:
    st.json(get_stock_info(keyword))
else:
    st.write("Use /?q=삼성전자 형태로 호출하세요.")
