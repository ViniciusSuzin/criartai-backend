from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Defina sua chave da OpenAI (substitua ou use via variável de ambiente)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-sua-chave-aqui")

@app.route("/gerar-anuncio", methods=["POST"])
def gerar_anuncio():
    data = request.json

    produto = data.get("produto", "")
    publico = data.get("publico", "")
    objetivo = data.get("objetivo", "")

    if not produto or not publico or not objetivo:
        return jsonify({"erro": "Campos obrigatórios ausentes."}), 400

    prompt = f"""
    Gere um texto de anúncio de tráfego pago para o Facebook/Instagram.
    Produto: {produto}
    Público-alvo: {publico}
    Objetivo: {objetivo}

    Use linguagem neutra, amigável e que respeite as políticas de publicidade da Meta (sem promessas exageradas, sem termos sensíveis).
    Gere apenas o texto do anúncio em no máximo 3 linhas.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        texto_gerado = response.choices[0].message.content.strip()
        return jsonify({"anuncio": texto_gerado})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

