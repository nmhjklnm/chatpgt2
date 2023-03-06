import openai
from io import BytesIO

#样式美化
import streamlit as st

# 添加博客链接
st.markdown("""
<a href="https://yang1he.gitee.io" target="_blank">作者链接</a>
""", unsafe_allow_html=True)

import streamlit as st

keys = ["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",
            "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",
            "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",
            "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",
            "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"
            ]

models = {
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301": "gpt-3.5-turbo-0301",
    }
# 添加菜单

def generate_response(prompt, model, index):
    openai.api_key = index
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ])

    message = response['choices'][0]['message']['content']
    # message = response.choices[0].text.strip()
    return message


def get_state():
    return {"chat_history": []}


def save_chat_history(chat_history):
    data = "\n".join(chat_history)
    b = BytesIO(data.encode())
    return st.download_button(label="Download chat history", data=b, file_name="chat_history.txt",
                              mime="text/plain")



menu = ["主页", "开发历史"]
choice = st.sidebar.selectbox("主页", menu)






if choice == "主页":

    st.title("")
    model = st.selectbox("选择模型", list(models.keys()))
    message = st.text_area("You", height=100, value="", key="input")



    if st.button("发送"):
        chat_history = st.session_state.state["chat_history"]
        # 清除重复聊天记录
        chat_history.append("You: " + message) if "You: " + message not in chat_history else chat_history.append(
            "You: " + "")
        index = len(chat_history) % len(keys)  # 使用取模操作来循环使用API key

        response = generate_response("\n".join(chat_history), models[model], keys[index])
        chat_history.append("ChatGPT: " + response)
        st.session_state.state["chat_history"] = chat_history

    if st.button("保存聊天记录"):
        st.write(save_chat_history(st.session_state.state["chat_history"]), unsafe_allow_html=True)

    if st.button("重开一个对话"):
        st.session_state.state = get_state()

    if "state" not in st.session_state:
        st.session_state.state = get_state()

    for msg in st.session_state.state["chat_history"]:
        st.markdown("---")
        st.write(msg)
    # for msg in st.session_state.state["chat_history"][len(chat_history):]:
    #         st.write(msg)
    #         st.markdown("---")



elif choice == "开发历史":
    st.title("2023年3月3：开始开发 ChatGPT Web")
    st.write("[2022年3月4：ChatGPT web v1.0 版本发布](https://gitee.com/yang1he/chatgpt-web-app)")
    st.write("[2022年3月5：ChatGPT web v2.0 版本发布](https://gitee.com/yang1he/chatgpt-web2-app)")
    st.empty()



def main():
    if "state" not in st.session_state:
        st.session_state.state = get_state()


if __name__ == "__main__":
    main()  # 调用主函数开始Streamlit应用
