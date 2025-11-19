import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Stock API")

# -------------------------------
# 1) 네이버 모바일 검색에서 종목코드 가져오기
# -------------------------------
def get_stock_code(query):
    url = f"https://m.search.naver.com/search.naver?query={query}+주가"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    # meta 태그에 종목 코드가 있음
    meta = soup.find("meta", {"property": "naverfinance:code"})
    if meta and meta.get("content"):
        return meta["content"]
    return None

# -------------------------------
# 2) 종목 정보 가져오기
# -------------------------------
def get_stock_info(keyword):
    code = get_stock_code(keyword)
    if not code:
        return {"error": "종목을 찾을 수 없음"}

    info_url = f"https://finance.naver.com/item/main.nhn?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r2 = requests.get(info_url, headers=headers)
    soup2 = BeautifulSoup(r2.text, "lxml")

    # 현재가
    today_tag = soup2.select_one("p.no_today span.blind")
    today = today_tag.text.strip() if today_tag else "N/A"

    # PER
    per_tag = soup2.select_one("table tbody tr td span.blind")
    per = per_tag.text.strip() if per_tag else "N/A"

    return {
        "name": keyword,
        "code": code,
        "price": today,
        "per": per,
        "link": info_url,
    }

# -------------------------------
# 3) Streamlit API 엔드포인트
# -------------------------------
keyword = st.query_params.get("q", "").strip()  # URL 파라미터 가져오기 + 공백 제거

if keyword:
    st.json(get_stock_info(keyword))
else:
    st.write("URL 뒤에 ?q=검색어 형태로 호출하세요. 예: ?q=삼성전자")
