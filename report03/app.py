import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("ToDo メモ管理アプリ")

# 新規追加
st.subheader("新規 ToDo 追加")
title = st.text_input("タイトル")
if st.button("追加"):
    res = requests.post(f"{API_URL}/todos", json={"title": title})
    st.write(res.json())

# 一覧表示
st.subheader("ToDo 一覧")
todos = requests.get(f"{API_URL}/todos").json()
for t in todos:
    st.write(f"{t['id']}: {t['title']} (done={t['done']})")

# 更新
st.subheader("更新")
update_id = st.number_input("更新するID", step=1)
new_title = st.text_input("新しいタイトル")
done = st.checkbox("完了した？")
if st.button("更新"):
    res = requests.put(
        f"{API_URL}/todos/{update_id}",
        json={"title": new_title, "done": done}
    )
    st.write(res.json())

# 削除
st.subheader("削除")
delete_id = st.number_input("削除するID", step=1, key="delete")
if st.button("削除"):
    res = requests.delete(f"{API_URL}/todos/{delete_id}")
    st.write(res.json())
