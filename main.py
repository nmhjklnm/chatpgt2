import streamlit as st  # 导入Streamlit库
import openai  # 导入OpenAI API库

# 设置OpenAI API密钥
openai.api_key = "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"
# 可选的模型列表
models = {
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301": "gpt-3.5-turbo-0301",
}

# 定义一个生成回复的函数
def generate_response(prompt, model):
    # 调用OpenAI API的Completion模块生成回复
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ])

    message = response['choices'][0]['message']['content']
    # message = response.choices[0].text.strip()
    return message


# 定义一个获取应用状态的函数
def get_state():
    return {"chat_history": []}

# 定义主函数
def main():
    # 在Streamlit应用中显示一个标题和一条简单的文本
    st.title("来和ChatGPT聊天")
    st.write("输入你的问题等待回复")

    # 如果“state”状态变量不存在，则调用get_state()函数获取应用状态
    if "state" not in st.session_state:
        st.session_state.state = get_state()

    # 显示一个下拉框，用于选择模型
    model = st.selectbox("选择模型", list(models.keys()))

    # 显示一个文本输入框，用户输入聊天内容
    message = st.text_area("You", height=100, value="", key="input")

    # 显示一个按钮，用于发送聊天内容
    if st.button("Send"):
        chat_history = st.session_state.state["chat_history"]  # 获取应用状态中的聊天记录
        chat_history.append("You: " + message)  # 将用户输入的内容添加到聊天记录中
        response = generate_response("\n".join(chat_history), models[model])  # 调用generate_response()函数生成回复
        chat_history.append("ChatGPT: " + response)  # 将生成的回复添加到聊天记录中
        st.session_state.state["chat_history"] = chat_history  # 更新应用状态中的聊天记录

    # 显示一个按钮，用于清除聊天记录
    if st.button("Clear chat history"):
        st.session_state.state = get_state()

    # 遍历应用状态中的聊天记录列表，并在Streamlit应用中显示每一条记录
    for msg in st.session_state.state["chat_history"]:
        st.write(msg)

if __name__ == "__main__":
    main()  # 调用主函数开始Streamlit应用
