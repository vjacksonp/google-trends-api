from flask import Flask, jsonify, request
from pytrends.request import TrendReq
import time

app = Flask(__name__)

# Configurar Pytrends con User-Agent y reintentos para evitar bloqueos
pytrends = TrendReq(
    hl="es",
    tz=360,
    retries=5,
    backoff_factor=2,
    requests_args={"headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}}
)

@app.route("/trends", methods=["GET"])
def get_trends():
    keyword = request.args.get("keyword", "")
    country = request.args.get("geo", "CL")  # CL = Chile

    if not keyword:
        return jsonify({"error": "Debes proporcionar una keyword"}), 400

    try:
        # Espera 5 segundos antes de hacer la solicitud para evitar bloqueos
        time.sleep(5)

        # Construir la solicitud de tendencias
        pytrends.build_payload([keyword], cat=0, timeframe="today 12-m", geo=country)
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"error": "No hay datos para esta keyword"}), 404

        # ✅ Convertir el índice Timestamp a string para evitar errores JSON
        data.index = data.index.astype(str)

        # ✅ Convertir a lista de diccionarios con "records"
        trends_list = data.drop(columns=["isPartial"]).reset_index().to_dict(orient="records")

        return jsonify({"keyword": keyword, "trends": trends_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

