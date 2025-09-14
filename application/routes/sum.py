from flask import Blueprint, request, jsonify
from application.summarize_tweets import summarize_tweets

sum_bp = Blueprint("sum_bp", __name__)

@sum_bp.route("/summarize", methods=["POST"])
def summarize_route():
    data = request.get_json()
    print("💡 Requête reçue:", data)
    match_name = data.get("match")  # Exemple : "Team A vs Team B"
    if not match_name:
        print("⚠️ Erreur: match name missing")
        return jsonify({"error": "match name required"}), 400

    result = summarize_tweets(match_name)
    print("✅ Résultat généré:", result) 
    return jsonify(result)
