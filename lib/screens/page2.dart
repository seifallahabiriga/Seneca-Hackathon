import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class MatchAnalysisScreen extends StatefulWidget {
  final String match;

  const MatchAnalysisScreen({super.key, required this.match});

  @override
  State<MatchAnalysisScreen> createState() => _MatchAnalysisScreenState();
}

class _MatchAnalysisScreenState extends State<MatchAnalysisScreen> {
  List<String> summaries = [];
  String predictedWinner = "TBD";

  Timer? _timer;

  @override
  void initState() {
    super.initState();
    // Timer toutes les 5 secondes
    _timer = Timer.periodic(
      const Duration(seconds: 5),
      (_) => _updateLiveData(),
    );
  }

  Future<void> _updateLiveData() async {
    try {
      // 1️⃣ Récupérer les tweets simulés pour l'instant
      List<String> tweets = [
        "12' Goal by Team A!",
        "15' Shot on target by Player X",
        "17' Corner kick for Team B",
        "20' Save by goalkeeper",
      ];

      print("🔄 Envoi de la requête pour le match: ${widget.match}");
      print("📤 Tweets envoyés: $tweets");

      // 2️⃣ Envoyer les tweets au backend Flask
      final response = await http.post(
        Uri.parse('http://10.118.75.134:5000/summarize'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({"match": widget.match}),
      );

      print("📥 Status code: ${response.statusCode}");
      print("📥 Body: ${response.body}");

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print("📊 Data décodée: $data");

        setState(() {
          predictedWinner = data['prediction'] ?? "TBD";

          String newSummary = data['summary'] ?? "";
          if (newSummary.isNotEmpty) {
            summaries.add(newSummary);
            if (summaries.length > 6) summaries.removeAt(0);
          }
        });
      } else {
        print("⚠️ Erreur backend: ${response.body}");
      }
    } catch (e) {
      print("❌ Erreur HTTP: $e");
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final teams = widget.match.split(" vs ");

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text(widget.match),
        backgroundColor: Colors.green[700],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Prédiction du gagnant
            Card(
              color: Colors.grey[900],
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Text(
                  "Predicted Winner: $predictedWinner",
                  style: const TextStyle(
                    color: Colors.greenAccent,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Summaries header
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                "Live Summary",
                style: TextStyle(
                  color: Colors.greenAccent[400],
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(height: 10),

            // Summaries feed
            Expanded(
              child: ListView.builder(
                itemCount: summaries.length,
                itemBuilder: (context, index) {
                  return Card(
                    color: Colors.grey[850],
                    margin: const EdgeInsets.symmetric(vertical: 6),
                    child: ListTile(
                      leading: const Icon(
                        Icons.sports_soccer,
                        color: Colors.greenAccent,
                      ),
                      title: Text(
                        summaries[index],
                        style: const TextStyle(color: Colors.white),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
