import re
from typing import List, Dict, Optional

class LiveMatchTracker:
    """Tracks live match events from text data (tweets, commentary)"""

    def __init__(self):
        self.events = {"events": []}
        self.stats = {
            "Corner Kicks_diff": 0,
            "Blocked Shots_diff": 0,
            "Shots on Goal_diff": 0,
            "Shots off Goal_diff": 0,
            "Goalkeeper Saves_diff": 0
        }
        self.recent_events = {"events": []}

    def extract_events_from_text(self, text_batch: List[str]) -> Dict:
        """Extract match events from text data using rule-based approach"""
        new_events = []

        for text in text_batch:
            text = text.lower()
            event = self._parse_single_text(text)
            if event:
                new_events.append(event)

        return {"events": new_events}

    def _parse_single_text(self, text: str) -> Optional[Dict]:
        """Parse a single text for match events"""
        time_pattern = r'(\d+)(?:\+(\d+))?[\'â€™]?'
        time_match = re.search(time_pattern, text)
        time_str = ""
        if time_match:
            base = int(time_match.group(1))
            extra = int(time_match.group(2)) if time_match.group(2) else 0
            time_str = f"{base}+{extra}" if extra > 0 else str(base)

        patterns = {
            'goal': [r'goal', r'scores', r'finds the net', r'into the goal'],
            'yellow_card': [r'yellow card', r'booked', r'cautioned'],
            'red_card': [r'red card', r'sent off', r'dismissed'],
            'save': [r'save', r'saved', r'keeper', r'goalkeeper'],
            'shot': [r'shot', r'shoots', r'effort'],
            'corner': [r'corner', r'corner kick'],
            'substitution': [r'substitution', r'replaced', r'comes on'],
            'offside': [r'offside', r'flagged'],
            'foul': [r'foul', r'fouled', r'free kick']
        }

        for event_type, keywords in patterns.items():
            if any(keyword in text for keyword in keywords):
                return {
                    "time": time_str,
                    "event": f"{event_type.replace('_', ' ').title()}: {text[:100]}"
                }

    def update_events(self, new_events: Dict):
        """Update the events list with new events"""
        if "event" in new_events:
            self.events["events"].append(new_events["event"])
            self.recent_events["events"].append(new_events["event"])
        elif "events" in new_events:
            self.events["events"].extend(new_events["events"])
            self.recent_events["events"].extend(new_events["events"])

    def generate_summary(self) -> Dict:
        """Generate summary of recent events"""
        if not self.recent_events["events"]:
            return {"summary": "No major events in this period.", "stats": self.stats.copy()}

        event_counts = {}
        for event in self.recent_events["events"]:
            event_text = event.get("event", "").lower()
            if "save" in event_text:
                event_counts["saves"] = event_counts.get("saves", 0) + 1
                self.stats["Goalkeeper Saves_diff"] += 1
                self.stats["Blocked Shots_diff"] += 1
            elif "shot" in event_text:
                event_counts["shots"] = event_counts.get("shots", 0) + 1
                if "on goal" in event_text or "on target" in event_text:
                    self.stats["Shots on Goal_diff"] += 1
                else:
                    self.stats["Shots off Goal_diff"] += 1
            elif "corner" in event_text:
                event_counts["corner"] = event_counts.get("corner", 0) + 1
                self.stats["Corner Kicks_diff"] += 1

        summary_parts = []
        for event_type, count in event_counts.items():
            summary_parts.append(f"{count} {event_type}")

        summary = f"Recent events: {', '.join(summary_parts)}" if summary_parts else "No major events."

        # Clear recent events after summary
        self.recent_events = {"events": []}

        return {"summary": summary, "stats": self.stats.copy()}
