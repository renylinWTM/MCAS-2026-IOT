import os
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from openai import OpenAI


# =========================
# Environment Variables
# =========================

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free",
)

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "找不到 OPENROUTER_API_KEY，請先建立 .env 並填入 API Key。"
    )

if not SECRET_KEY or SECRET_KEY == "CHANGE_ME":
    raise RuntimeError(
        "請在 .env 設定安全的 SECRET_KEY。"
    )


# =========================
# Flask
# =========================

app = Flask(__name__)
app.secret_key = SECRET_KEY


# Lab 用簡化帳號
# 正式系統不應以明文保存密碼
USERS = {
    "admin": "1234",
}


# =========================
# OpenAI
# =========================

openrouter_client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def ask_openrouter(
    message,
    history=None,
):
    history = history or []

    messages = [
        {
            "role": "system",
            "content": (
                "你是 Lab6 聊天網站的 AI 助手。"
                "這個網站透過 OpenRouter API 串接 AI 模型。"
                f"目前設定的路由模型是 {OPENROUTER_MODEL}。"
                "如果使用者詢問你使用什麼 API，"
                "請回答：此網站透過 OpenRouter API 提供 AI 回覆。"
                "不要宣稱自己固定是 Gemini 或特定 GPT 型號，"
                "因為 openrouter/free 可能選用不同的免費模型。"
            ),
        }
    ]

    for item in history[-4:]:
        role = item.get("role")
        content = str(
            item.get("content", "")
        ).strip()

        if (
            role in {"user", "assistant"}
            and content
        ):
            messages.append({
                "role": role,
                "content": content,
            })

    messages.append({
        "role": "user",
        "content": message,
    })

    completion = (
        openrouter_client
        .chat
        .completions
        .create(
            model=OPENROUTER_MODEL,
            messages=messages,
        )
    )

    reply = (
        completion
        .choices[0]
        .message
        .content
        or ""
    ).strip()

    if not reply:
        reply = "OpenRouter 沒有回傳文字內容。"

    return reply


# =========================
# Login Required
# =========================

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user" not in session:

            # API 不做 redirect
            if request.path.startswith("/api/"):
                return jsonify({
                    "error": "請先登入"
                }), 401

            return redirect(
                url_for("login")
            )

        return view(*args, **kwargs)

    return wrapped


# =========================
# Login
# =========================

@app.route(
    "/",
    methods=["GET", "POST"],
)
def login():

    if request.method == "POST":

        username = (
            request.form
            .get("username", "")
            .strip()
        )

        password = request.form.get(
            "password",
            "",
        )

        if (
            username in USERS
            and USERS[username] == password
        ):

            session.clear()

            session["user"] = username

            return redirect(
                url_for("chat_room")
            )

        return render_template(
            "login.html",
            msg="帳號或密碼錯誤",
        )

    if "user" in session:
        return redirect(
            url_for("chat_room")
        )

    return render_template(
        "login.html"
    )


# =========================
# Chat Page
# =========================

@app.get("/chat")
@login_required
def chat_room():

    return render_template(
        "chat.html",
        username=session["user"],
    )


# =========================
# OpenAI API
# =========================

@app.post("/api/chat")
@login_required
def api_chat():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    message = str(
        data.get("message", "")
    ).strip()

    if not message:
        return jsonify({
            "error": "訊息不可為空"
        }), 400

    if len(message) > 2000:
        return jsonify({
            "error": "訊息過長"
        }), 400

    try:

        history = session.get(
            "chat_history",
            [],
        )

        reply = ask_openrouter(
            message,
            history,
        )

        history.extend([
            {
                "role": "user",
                "content": message[:700],
            },
            {
                "role": "assistant",
                "content": reply[:700],
            },
        ])

        session["chat_history"] = (
            history[-4:]
        )

        return jsonify({
            "reply": reply
        })

    except Exception as error:

        print(
            "[OpenAI API Error]","[OpenRouter API Error]",
            error,
        )

        return jsonify({
            "error":
            "OpenAI API 呼叫失敗，"
            "請檢查 API Key、網路或模型設定。"
        }), 502


# =========================
# Reset Conversation
# =========================

@app.post("/api/reset")
@login_required
def reset_chat():

    session.pop(
        "chat_history",
        None,
    )

    return jsonify({
        "ok": True
    })


# =========================
# Logout
# =========================

@app.post("/logout")
@login_required
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================
# Run Server
# =========================

if __name__ == "__main__":

    print(
        "=== Lab6 Flask Server ==="
    )

    print(
        "Listening on "
        "http://0.0.0.0:3000"
    )

    print(
        "Debug mode is OFF"
    )

    app.run(
        host="0.0.0.0",
        port=3000,
        debug=False,
    )
