import streamlit as st
from crawling import finance_naver
from public_bike import bikes_da
from meteor_shower import meteor_shower


# 사이드바 화면

st.sidebar.header('로그인')
user_id = st.sidebar.text_input('아이디 입력',value='streamlit',max_chars=15)
user_password = st.sidebar.text_input('패스워드 입력', value='1234',type='password')

if user_password == '1234':
    st.sidebar.header('?의 포트폴리오')
    opt_data = ['','환율조회','따릉이','유성우']
    menu = st.sidebar.selectbox('메뉴 선택', opt_data, index=0)
    st.sidebar.write('선택한 메뉴:',menu)
    
    if menu == '환율조회':
        st.subheader('환율조회 >>>>>>>>>')
        finance_naver.exchange_main()
    
    elif menu == '따릉이':
        st.subheader('따릉이 데이터분석 >>>>>>>>>')
        bikes_da.bikes_da()
        
    elif menu == '유성우':
        st.subheader('유성우 데이터 분석 >>>>>>>>>')
        meteor_shower.meteor_main()
        
    else:
        st.subheader('?의 페이지:100:에 오신 것을 환영합니다.')

