import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": ["https://shun09070.github.io"]}})

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.7-flash")
SYSTEM = """あなたはmonrêve専属AIマネージャーです。
制作、販売、在庫、経費、発信、イベント、注文、タスクを横断分析してください。
日本語で、結論→理由→具体的な次の行動の順に、実行しやすく回答してください。
データがないことは推測で断定しないでください。"""

@app.get("/")
def health():
    return {"status":"ok"}

@app.post("/analyze")
def analyze():
    data=request.get_json(silent=True) or {}
    prompt=str(data.get("prompt","")).strip()
    if not prompt:
        return jsonify(error="相談内容がありません"),400
    if len(prompt)>30000:
        return jsonify(error="相談内容が長すぎます"),400
    try:
        r=client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM,
                temperature=0.4,
                max_output_tokens=1800,
            ),
        )
        return jsonify(answer=r.text or "")
    except Exception:
        app.logger.exception("Gemini error")
        return jsonify(error="Gemini APIへの接続に失敗しました"),500
