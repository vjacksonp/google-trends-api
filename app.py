from flask import Flask, jsonify, request
from pytrends.request import TrendReq

app = Flask(__name__)  # 📌 Define correctamente la aplicación Flask
pytrends = TrendReq(hl='es', tz=360)

@app.route('/trends', methods=['GET'])
def get_trends():
    keyword = request.args.get('keyword', '')
    country = request.args.get('geo', 'CL')  # CL = Chile (puedes cambiarlo)

    if not keyword:
        return jsonify({"error": "Debes proporcionar una keyword"}), 400

    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo=country)
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"error": "No hay datos para esta keyword"}), 404

        return jsonify(data.to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 📌 Asegúrate de que esto esté en el código

