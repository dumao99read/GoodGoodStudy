import os
import json
import uuid
import logging
import random
from datetime import datetime
from typing import Optional

from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

# ---------- logging ----------
LOG_DIR = os.path.join(CURRENT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(CURRENT_DIR, "guess_historyor.log")

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

# ---------- game records storage ----------
RECORDS_DIR = os.path.join(CURRENT_DIR, "records")


def _ensure_dir():
    os.makedirs(RECORDS_DIR, exist_ok=True)


def _record_path(game_id: str) -> str:
    return os.path.join(RECORDS_DIR, f"{game_id}.json")


def _next_game_number():
    _ensure_dir()
    max_num = 0
    for filename in os.listdir(RECORDS_DIR):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(RECORDS_DIR, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
            num = data.get("game_number", 0)
            if num > max_num:
                max_num = num
        except (json.JSONDecodeError, KeyError):
            continue
    return max_num + 1


def list_games():
    _ensure_dir()
    games = []
    for filename in os.listdir(RECORDS_DIR):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(RECORDS_DIR, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
            games.append({
                "id": data["id"],
                "game_number": data["game_number"],
                "figure_name": data.get("figure_name", "???"),
                "won": data.get("won"),
                "finished": data.get("finished", False),
                "hints_used": data.get("hints_used", 0),
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
            })
        except (json.JSONDecodeError, KeyError):
            continue
    games.sort(key=lambda x: x["created_at"], reverse=True)
    return games


def get_record(game_id: str):
    _ensure_dir()
    path = _record_path(game_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_record(data: dict):
    _ensure_dir()
    data["updated_at"] = datetime.now().isoformat()
    with open(_record_path(data["id"]), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def delete_record(game_id: str) -> bool:
    _ensure_dir()
    path = _record_path(game_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


# ---------- figure generation ----------
FALLBACK_FIGURES = [
    {"name": "嬴政", "aliases": ["秦始皇", "始皇帝"], "dynasty": "秦朝", "identity": "皇帝", "surname": "嬴"},
    {"name": "刘邦", "aliases": ["汉高祖"], "dynasty": "汉朝", "identity": "皇帝", "surname": "刘"},
    {"name": "刘彻", "aliases": ["汉武帝"], "dynasty": "汉朝", "identity": "皇帝", "surname": "刘"},
    {"name": "李世民", "aliases": ["唐太宗"], "dynasty": "唐朝", "identity": "皇帝", "surname": "李"},
    {"name": "赵匡胤", "aliases": ["宋太祖"], "dynasty": "宋朝", "identity": "皇帝", "surname": "赵"},
    {"name": "朱元璋", "aliases": ["明太祖"], "dynasty": "明朝", "identity": "皇帝", "surname": "朱"},
    {"name": "康熙", "aliases": ["清圣祖"], "dynasty": "清朝", "identity": "皇帝", "surname": "爱新觉罗"},
    {"name": "诸葛亮", "aliases": ["孔明", "卧龙"], "dynasty": "三国", "identity": "政治家、军事家", "surname": "诸葛"},
    {"name": "魏徵", "aliases": [], "dynasty": "唐朝", "identity": "宰相", "surname": "魏"},
    {"name": "王安石", "aliases": ["王介甫"], "dynasty": "宋朝", "identity": "政治家、文学家", "surname": "王"},
    {"name": "包拯", "aliases": ["包青天", "包公"], "dynasty": "宋朝", "identity": "清官", "surname": "包"},
    {"name": "张居正", "aliases": [], "dynasty": "明朝", "identity": "政治家、改革家", "surname": "张"},
    {"name": "海瑞", "aliases": ["海青天"], "dynasty": "明朝", "identity": "清官", "surname": "海"},
    {"name": "韩信", "aliases": [], "dynasty": "汉朝", "identity": "军事家、武将", "surname": "韩"},
    {"name": "关羽", "aliases": ["关云长", "关公", "武圣"], "dynasty": "三国", "identity": "武将", "surname": "关"},
    {"name": "岳飞", "aliases": ["岳武穆"], "dynasty": "宋朝", "identity": "抗金名将", "surname": "岳"},
    {"name": "戚继光", "aliases": [], "dynasty": "明朝", "identity": "抗倭名将", "surname": "戚"},
    {"name": "霍去病", "aliases": [], "dynasty": "汉朝", "identity": "将领", "surname": "霍"},
    {"name": "李靖", "aliases": ["李药师"], "dynasty": "唐朝", "identity": "军事家、将领", "surname": "李"},
    {"name": "孔子", "aliases": ["孔丘", "仲尼"], "dynasty": "春秋", "identity": "思想家、教育家", "surname": "孔"},
    {"name": "孟子", "aliases": ["孟轲"], "dynasty": "战国", "identity": "思想家", "surname": "孟"},
    {"name": "老子", "aliases": ["李耳", "老聃"], "dynasty": "春秋", "identity": "哲学家", "surname": "李"},
    {"name": "庄子", "aliases": ["庄周"], "dynasty": "战国", "identity": "思想家、文学家", "surname": "庄"},
    {"name": "朱熹", "aliases": ["朱子"], "dynasty": "宋朝", "identity": "理学家", "surname": "朱"},
    {"name": "王阳明", "aliases": ["王守仁"], "dynasty": "明朝", "identity": "哲学家、军事家", "surname": "王"},
    {"name": "屈原", "aliases": ["屈平"], "dynasty": "战国", "identity": "诗人", "surname": "屈"},
    {"name": "李白", "aliases": ["李太白", "诗仙"], "dynasty": "唐朝", "identity": "诗人", "surname": "李"},
    {"name": "杜甫", "aliases": ["杜子美", "诗圣"], "dynasty": "唐朝", "identity": "诗人", "surname": "杜"},
    {"name": "苏轼", "aliases": ["苏东坡", "苏子瞻"], "dynasty": "宋朝", "identity": "文学家、词人", "surname": "苏"},
    {"name": "辛弃疾", "aliases": ["辛幼安"], "dynasty": "宋朝", "identity": "词人、将领", "surname": "辛"},
    {"name": "李清照", "aliases": ["易安居士"], "dynasty": "宋朝", "identity": "女词人", "surname": "李"},
    {"name": "曹雪芹", "aliases": [], "dynasty": "清朝", "identity": "文学家", "surname": "曹"},
    {"name": "罗贯中", "aliases": [], "dynasty": "元末明初", "identity": "小说家", "surname": "罗"},
    {"name": "施耐庵", "aliases": [], "dynasty": "元末明初", "identity": "小说家", "surname": "施"},
    {"name": "吴承恩", "aliases": [], "dynasty": "明朝", "identity": "小说家", "surname": "吴"},
    {"name": "商鞅", "aliases": ["公孙鞅", "卫鞅"], "dynasty": "战国", "identity": "政治家、改革家", "surname": "公孙"},
    {"name": "曹操", "aliases": ["曹孟德"], "dynasty": "三国", "identity": "政治家、军事家、文学家", "surname": "曹"},
    {"name": "管仲", "aliases": [], "dynasty": "春秋", "identity": "政治家", "surname": "管"},
    {"name": "孙悟空", "aliases": ["齐天大圣", "美猴王"], "dynasty": "唐代（小说）", "identity": "小说人物", "surname": "孙"},
    {"name": "贾宝玉", "aliases": ["宝二爷"], "dynasty": "清代（小说）", "identity": "小说人物", "surname": "贾"},
    {"name": "武松", "aliases": ["武二郎"], "dynasty": "宋代（小说）", "identity": "小说人物", "surname": "武"},
    {"name": "林冲", "aliases": ["豹子头"], "dynasty": "宋代（小说）", "identity": "小说人物", "surname": "林"},
    {"name": "赵云", "aliases": ["赵子龙", "常山赵子龙"], "dynasty": "三国", "identity": "武将", "surname": "赵"},
    {"name": "周瑜", "aliases": ["周公瑾"], "dynasty": "三国", "identity": "将领、谋士", "surname": "周"},
    {"name": "项羽", "aliases": ["西楚霸王"], "dynasty": "秦末", "identity": "军事家、将领", "surname": "项"},
    {"name": "孙武", "aliases": ["孙子"], "dynasty": "春秋", "identity": "军事家", "surname": "孙"},
    {"name": "韩非", "aliases": ["韩非子"], "dynasty": "战国", "identity": "思想家、法家代表", "surname": "韩"},
    {"name": "陶渊明", "aliases": ["陶潜", "五柳先生"], "dynasty": "东晋", "identity": "诗人、隐士", "surname": "陶"},
    {"name": "玄奘", "aliases": ["唐僧", "三藏法师"], "dynasty": "唐朝", "identity": "高僧、翻译家", "surname": "陈"},
    {"name": "郑和", "aliases": ["三宝太监"], "dynasty": "明朝", "identity": "航海家", "surname": "马"},
    {"name": "花木兰", "aliases": [], "dynasty": "南北朝", "identity": "巾帼英雄（文学人物）", "surname": "花"},
]

_used_figures = set()


def _pick_figure_via_llm():
    used_list = "、".join(sorted(_used_figures)) if _used_figures else "无"

    prompt = f"""请随机生成一位中国古代或近代的历史名人（包括皇帝、文臣、武将、思想家、文学家、政治家等）或经典小说人物。

已生成过的人物：{used_list}

请严格按照以下JSON格式返回，不要包含任何其他内容，确保JSON合法：
{{"name": "人物主要姓名", "aliases": ["常见别名1", "常见别名2"], "dynasty": "所属朝代", "identity": "身份标签", "surname": "姓氏"}}

要求：
1. name必须是人物最常用的正式姓名或称号
2. aliases包含其他常见称呼（如没有则填空数组）
3. identity如：皇帝、宰相、诗人、武将、思想家等
4. 每次生成不同的人物，不要与已生成过的重复
5. 人物要具有代表性，广为人知
6. 姓名必须是全名"""
    try:
        msgs = [
            SystemMessage(content="你是一个中国历史名人生成器，只输出合法JSON，不要输出其他内容。"),
            HumanMessage(content=prompt)
        ]
        response = llm.invoke(msgs)
        content = response.content.strip()
        start = content.index("{")
        end = content.rindex("}") + 1
        data = json.loads(content[start:end])
        name = data.get("name", "").strip()
        if name and name not in _used_figures:
            _used_figures.add(name)
            return {
                "name": name,
                "aliases": data.get("aliases", []),
                "dynasty": data.get("dynasty", "未知"),
                "identity": data.get("identity", "未知"),
                "surname": data.get("surname", "未知"),
            }
    except Exception as e:
        logging.warning(f"LLM figure generation failed: {e}")
    return None


def _pick_figure_fallback():
    available = [f for f in FALLBACK_FIGURES if f["name"] not in _used_figures]
    if not available:
        _used_figures.clear()
        available = list(FALLBACK_FIGURES)
    chosen = random.choice(available)
    _used_figures.add(chosen["name"])
    return chosen


def generate_figure():
    figure = _pick_figure_via_llm()
    if figure is None:
        figure = _pick_figure_fallback()
    return figure


# ---------- app & llm ----------
app = Flask(__name__)

llm = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model=MODEL,
)


def log_api_call(endpoint: str, status: int, **extra):
    extra_str = " | ".join(f"{k}={v}" for k, v in extra.items() if v)
    logging.info(f"[{endpoint}] status={status} | {extra_str}")


# ---------- serve frontend ----------
@app.route("/")
def index():
    return send_from_directory(CURRENT_DIR, "index.html")


@app.route("/api/games", methods=["GET"])
def get_games():
    return jsonify(list_games())


@app.route("/api/game/new", methods=["POST"])
def new_game():
    figure = generate_figure()
    game_id = str(uuid.uuid4())
    game_number = _next_game_number()
    now = datetime.now().isoformat()
    record = {
        "id": game_id,
        "game_number": game_number,
        "figure_name": figure["name"],
        "aliases": figure.get("aliases", []),
        "dynasty": figure["dynasty"],
        "identity": figure["identity"],
        "surname": figure["surname"],
        "hints_used": 0,
        "hints": [],
        "guesses": [],
        "won": None,
        "finished": False,
        "created_at": now,
        "updated_at": now,
    }
    save_record(record)
    log_api_call("new_game", 200, game_id=game_id, game_number=game_number, figure=figure["name"])
    return jsonify({
        "id": game_id,
        "game_number": game_number,
        "hints_used": 0,
        "hints": [],
        "finished": False,
    }), 201


@app.route("/api/game/<game_id>", methods=["GET"])
def get_game_state(game_id):
    record = get_record(game_id)
    if not record:
        return jsonify({"error": "游戏不存在"}), 404
    return jsonify({
        "id": record["id"],
        "game_number": record["game_number"],
        "figure_name": record["figure_name"] if record.get("finished") else None,
        "won": record.get("won"),
        "finished": record.get("finished", False),
        "hints_used": record.get("hints_used", 0),
        "hints": record.get("hints", []),
        "guesses": record.get("guesses", []),
        "created_at": record["created_at"],
    })


@app.route("/api/game/<game_id>/hint", methods=["POST"])
def get_hint(game_id):
    record = get_record(game_id)
    if not record:
        return jsonify({"error": "游戏不存在"}), 404
    if record.get("finished"):
        return jsonify({"error": "游戏已结束"}), 400

    hints_used = record.get("hints_used", 0)

    if hints_used >= 3:
        record["finished"] = True
        record["won"] = False
        record["hints_used"] = hints_used + 1
        save_record(record)
        log_api_call("hint_reveal", 200, game_id=game_id, figure=record["figure_name"])
        return jsonify({
            "game_over": True,
            "won": False,
            "answer": record["figure_name"],
            "hints_used": record["hints_used"],
            "message": f"游戏结束！答案是 {record['figure_name']}"
        })

    hint_keys = ["dynasty", "identity", "surname"]
    hint_labels = {"dynasty": "朝代", "identity": "身份", "surname": "姓氏"}
    hint_key = hint_keys[hints_used]
    hint_text = f"{hint_labels[hint_key]}：{record[hint_key]}"

    record["hints_used"] = hints_used + 1
    if "hints" not in record:
        record["hints"] = []
    record["hints"].append(hint_text)
    save_record(record)

    log_api_call("hint", 200, game_id=game_id, hint_index=hints_used)
    return jsonify({
        "game_over": False,
        "hint": hint_text,
        "hints_used": record["hints_used"],
        "hints": record["hints"],
    })


@app.route("/api/game/<game_id>/guess", methods=["POST"])
def make_guess(game_id):
    data = request.get_json(silent=True) or {}
    guess = data.get("guess", "").strip()

    if not guess:
        return jsonify({"error": "请输入你的猜测"}), 400

    record = get_record(game_id)
    if not record:
        return jsonify({"error": "游戏不存在"}), 404
    if record.get("finished"):
        return jsonify({"error": "游戏已结束"}), 400

    names_to_check = {record["figure_name"]}
    for alias in record.get("aliases", []):
        if alias:
            names_to_check.add(alias)

    correct = guess in names_to_check

    if "guesses" not in record:
        record["guesses"] = []
    record["guesses"].append({
        "guess": guess,
        "correct": correct,
        "timestamp": datetime.now().isoformat(),
    })

    if correct:
        record["finished"] = True
        record["won"] = True
        save_record(record)
        log_api_call("guess_correct", 200, game_id=game_id, figure=record["figure_name"])
        return jsonify({
            "correct": True,
            "game_over": True,
            "won": True,
            "answer": record["figure_name"],
            "message": f"恭喜你猜对了！答案是 {record['figure_name']}"
        })

    save_record(record)
    return jsonify({
        "correct": False,
        "game_over": False,
        "message": "不对，再想想！"
    })


@app.route("/api/game/<game_id>", methods=["DELETE"])
def remove_game(game_id):
    if not delete_record(game_id):
        return jsonify({"error": "游戏不存在"}), 404
    log_api_call("delete_game", 200, game_id=game_id)
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = 5001
    print(f"打开游戏，请访问网址: http://localhost:{port}")
    logging.info("Guess Historyor started")
    app.run(host="0.0.0.0", port=port, debug=False)
