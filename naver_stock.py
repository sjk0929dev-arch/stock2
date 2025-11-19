import streamlit as st
import FinanceDataReader as fdr

st.set_page_config(page_title="Stock API")

def get_stock_info(ticker):
    """
    FDR을 사용해서 주가와 기본 정보 가져오기
    """
    try:
        df = fdr.DataReader(ticker)  # 기본적으로 최근 1년 데이터
        if df.empty:
            return {"error": "종목 정보를 찾을 수 없음"}
        
        # 최근 거래일 기준 데이터
        latest = df.iloc[-1]

        return {
            "ticker": ticker,
            "date": str(latest.name.date()),
            "open": latest["Open"],
            "high": latest["High"],
            "low": latest["Low"],
            "close": latest["Close"],
            "volume": int(latest["Volume"]),
            "link": f"https://finance.naver.com/item/main.nhn?code={ticker}"  # 참고용 링크
        }
    except Exception as e:
        return {"error": str(e)}

# Streamlit API 엔드포인트
ticker = st.query_params.get("q", "").strip().upper()  # 티커는 대문자

if ticker:
    st.json(get_stock_info(ticker))
else:
    st.write("URL 뒤에 ?q=티커 형태로 호출하세요. 예: ?q=005930")
