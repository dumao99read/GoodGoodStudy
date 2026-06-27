import os
import json
import uuid
import logging
from datetime import datetime
from typing import Optional

from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

# ---------- logging ----------
LOG_DIR = os.path.join(CURRENT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(CURRENT_DIR, f"chatAgent.log")

logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    filemode='w',
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# ---------- config validation ----------
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("OPENAI_MODEL")

missing = []
if not API_KEY:
    missing.append("OPENAI_API_KEY")
if not BASE_URL:
    missing.append("OPENAI_BASE_URL")
if not MODEL:
    missing.append("OPENAI_MODEL")
if missing:
    logging.error(f"Missing environment variables: {', '.join(missing)}")
    raise SystemExit(f"请检查 .env 文件，缺少必要配置: {', '.join(missing)}")

# ---------- conversation storage ----------
CONVERSATIONS_DIR = os.path.join(CURRENT_DIR, "conversations")


def _ensure_dir():
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)


def _conv_path(conv_id: str) -> str:
    return os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")


def list_conversations():
    _ensure_dir()
    conversations = []
    for filename in os.listdir(CONVERSATIONS_DIR):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(CONVERSATIONS_DIR, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
            conversations.append({
                "id": data["id"],
                "name": data["name"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "message_count": len(data.get("messages", [])),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    conversations.sort(key=lambda x: x["updated_at"], reverse=True)
    return conversations


def create_conversation(name: Optional[str] = None):
    _ensure_dir()
    conv_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    if not name:
        name = f"新对话 {datetime.now().strftime('%m/%d %H:%M')}"
    data = {
        "id": conv_id,
        "name": name,
        "created_at": now,
        "updated_at": now,
        "messages": [],
    }
    with open(_conv_path(conv_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"id": conv_id, "name": name, "created_at": now, "updated_at": now, "message_count": 0}


def delete_conversation(conv_id: str) -> bool:
    _ensure_dir()
    path = _conv_path(conv_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def rename_conversation(conv_id: str, new_name: str) -> bool:
    _ensure_dir()
    path = _conv_path(conv_id)
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["name"] = new_name
    data["updated_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def get_conversation(conv_id: str):
    _ensure_dir()
    path = _conv_path(conv_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_message(conv_id: str, role: str, content: str) -> bool:
    _ensure_dir()
    path = _conv_path(conv_id)
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })
    data["updated_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


# ---------- app & llm ----------
app = Flask(__name__)

llm = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model=MODEL,
)

SYSTEM_PROMPT = "你是一个有用的AI助手，请用中文回答用户的问题。"


def log_api_call(endpoint: str, status: int, **extra):
    extra_str = " | ".join(f"{k}={v}" for k, v in extra.items() if v)
    logging.info(f"[{endpoint}] status={status} | {extra_str}")


def build_messages(conv_data: dict):
    msgs = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in conv_data.get("messages", []):
        if m["role"] == "user":
            msgs.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            msgs.append(AIMessage(content=m["content"]))
    return msgs


# ---------- serve frontend ----------
@app.route("/")
def index():
    return send_from_directory(CURRENT_DIR, "index.html")


@app.route("/api/conversations", methods=["GET"])
def get_conversations():
    return jsonify(list_conversations())


@app.route("/api/conversations", methods=["POST"])
def new_conversation():
    data = request.get_json(silent=True) or {}
    conv = create_conversation(data.get("name"))
    log_api_call("create_conversation", 200, conv_id=conv["id"], name=conv["name"])
    return jsonify(conv), 201


@app.route("/api/conversations/<conv_id>", methods=["DELETE"])
def remove_conversation(conv_id):
    if not delete_conversation(conv_id):
        return jsonify({"error": "对话不存在"}), 404
    log_api_call("delete_conversation", 200, conv_id=conv_id)
    return jsonify({"ok": True})


@app.route("/api/conversations/<conv_id>", methods=["PATCH"])
def update_conversation(conv_id):
    data = request.get_json(silent=True) or {}
    new_name = data.get("name")
    if not new_name:
        return jsonify({"error": "请输入新名称"}), 400
    if not rename_conversation(conv_id, new_name):
        return jsonify({"error": "对话不存在"}), 404
    log_api_call("rename_conversation", 200, conv_id=conv_id, new_name=new_name)
    return jsonify({"ok": True})


@app.route("/api/conversations/<conv_id>/messages", methods=["GET"])
def get_messages(conv_id):
    conv = get_conversation(conv_id)
    if not conv:
        return jsonify({"error": "对话不存在"}), 404
    return jsonify(conv["messages"])


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    conv_id = data.get("conversation_id", "")

    if not question:
        return jsonify({"error": "请输入问题"}), 400
    if not conv_id:
        return jsonify({"error": "缺少 conversation_id"}), 400

    conv = get_conversation(conv_id)
    if not conv:
        return jsonify({"error": "对话不存在"}), 404

    add_message(conv_id, "user", question)

    try:
        messages = build_messages(conv)
        messages.append(HumanMessage(content=question))

        response = llm.invoke(messages)
        answer = response.content

        add_message(conv_id, "assistant", answer)

        log_api_call("chat", 200, conv_id=conv_id, question_len=len(question), answer_len=len(answer))
        return jsonify({"answer": answer})
    except Exception as e:
        logging.error(f"[chat] conv_id={conv_id} error={str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logging.info("Chat agent started")
    app.run(host="0.0.0.0", port=5000, debug=False)
