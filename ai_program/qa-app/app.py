import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = Flask(__name__)

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY", 'sk-b5941b55653842e6b891415d540ce5ec'),
    base_url=os.getenv("OPENAI_BASE_URL", 'https://dashscope.aliyuncs.com/apps/anthropic/v1'),
    model=os.getenv("OPENAI_MODEL", "Qwen3 Coder Plus"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的AI助手，请用中文回答用户的问题。"),
    ("human", "{question}"),
])

chain = prompt | llm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "请输入问题"}), 400

    try:
        response = chain.invoke({"question": question})
        return jsonify({"answer": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
