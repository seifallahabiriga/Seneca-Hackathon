import 'package:flutter/material.dart';
import 'page2.dart';

class HomeScreen extends StatelessWidget {
  HomeScreen({super.key});

  final List<Map<String, String>> matches = [
    {"home": "FC Barcelona", "away": "Real Madrid", "time": "21:00"},
    {"home": "PSG", "away": "OM", "time": "20:45"},
    {"home": "Liverpool", "away": "Man City", "time": "22:00"},
    {
      "home": "Manchester City",
      "away": "Inter Milano",
      "time":
          "${DateTime.now().hour.toString().padLeft(2, '0')}:${DateTime.now().minute.toString().padLeft(2, '0')}",
    },
    {"home": "Bayern Munich", "away": "Dortmund", "time": "19:30"},
    {"home": "Juventus", "away": "AC Milan", "time": "20:00"},
  ];

  @override
  Widget build(BuildContext context) {
    // mettre Man City vs Inter en haut
    matches.sort((a, b) {
      if (a['home'] == "Manchester City" && a['away'] == "Inter Milano") {
        return -1;
      }
      if (b['home'] == "Manchester City" && b['away'] == "Inter Milano") {
        return 1;
      }
      return 0;
    });

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text("⚽ Match Center"),
        centerTitle: true,
        backgroundColor: Colors.green,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Choisissez un match à analyser",
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 20),

            Expanded(
              child: ListView.builder(
                itemCount: matches.length,
                itemBuilder: (context, index) {
                  final match = matches[index];

                  // convertir heure en DateTime
                  final matchTimeParts = match['time']!.split(':');
                  final matchHour = int.parse(matchTimeParts[0]);
                  final matchMinute = int.parse(matchTimeParts[1]);
                  final now = DateTime.now();
                  final matchDateTime = DateTime(
                    now.year,
                    now.month,
                    now.day,
                    matchHour,
                    matchMinute,
                  );

                  final isLive =
                      now.isAfter(matchDateTime) &&
                      now.isBefore(
                        matchDateTime.add(const Duration(minutes: 90)),
                      );

                  final timeColor = isLive
                      ? Colors.greenAccent
                      : Colors.redAccent;

                  return GestureDetector(
                    onTap: () {
                      if (!isLive) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text("Match non encore commencé"),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      } else {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => MatchAnalysisScreen(
                              match: "${match['home']} vs ${match['away']}",

                            ),
                          ),
                        );
                      }
                    },
                    child: Card(
                      color: Colors.grey[900],
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      margin: const EdgeInsets.symmetric(vertical: 10),
                      child: ListTile(
                        leading: const Icon(
                          Icons.sports_soccer,
                          color: Colors.greenAccent,
                          size: 32,
                        ),
                        title: Text(
                          "${match['home']} vs ${match['away']}",
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        subtitle: Text(
                          "Heure : ${match['time']}",
                          style: TextStyle(color: timeColor),
                        ),
                        trailing: const Icon(
                          Icons.arrow_forward_ios,
                          color: Colors.greenAccent,
                        ),
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
