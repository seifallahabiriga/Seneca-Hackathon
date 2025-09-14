from application.models import predict_from_dict
from application.models.tweet import Tweet
from live_match_tracker import LiveMatchTracker

tracker = LiveMatchTracker()

def summarize_tweets(match_name):
    # 1️⃣ Récupérer les tweets depuis PostgreSQL
    tweets_query = Tweet.query.filter_by(match=match_name).order_by(Tweet.timestamp.asc()).all()
    tweets_text = [t.tweet for t in tweets_query]

    # 2️⃣ Extraire les événements
    events = tracker.extract_events_from_text(tweets_text)
    tracker.update_events(events)

    # 3️⃣ Générer résumé et stats
    summary_stats = tracker.generate_summary()

    # 4️⃣ Prédire le gagnant (0 = équipe A, 1 = équipe B)
    prediction_raw = predict_from_dict(summary_stats["stats"])
    try:
        team_a, team_b = match_name.split(" vs ")
    except ValueError:
        team_a, team_b = "Team A", "Team B"  # fallback

    predicted_winner = team_a if prediction_raw == 0 else team_b

    # 5️⃣ Retourner un dictionnaire JSON
    return {
        "summary": summary_stats["summary"],
        "stats": summary_stats["stats"],
        "prediction": predicted_winner   # ⚠️ string au lieu de 0/1
    }
