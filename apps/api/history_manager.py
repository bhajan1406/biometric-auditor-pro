"""
History Manager - Biometric Auditor V2
Tracks and analyzes historical biometric data and workout patterns.
"""
"""
History Manager - Biometric Auditor V2
Tracks and analyzes historical biometric data and workout patterns.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv
import opik
from opik import track

# Load environment variables
load_dotenv()

# Define the data storage path
DATA_DIR = Path(__file__).parent / "data"
HISTORY_FILE = DATA_DIR / "biometric_history.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
class HistoryManager:
    """Manages biometric and workout history with JSON persistence."""
    
    def __init__(self, history_file: Path = HISTORY_FILE):
        self.history_file = history_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create history file if it doesn't exist."""
        if not self.history_file.exists():
            self._save_history({"users": {}})
    
    def _load_history(self) -> dict:
        """Load history from JSON file."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"users": {}}
    
    def _save_history(self, data: dict):
        """Save history to JSON file."""
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    @track
    def add_entry(
        self, 
        user_id: str,
        biometrics: dict,
        compliance: dict,
        workout_plan: str,
        recommendation: str,
        completed: bool = False
    ) -> dict:
        """
        Add a new biometric entry to history.
        
        Args:
            user_id: User identifier
            biometrics: Biometric data (sleep, hr, recovery_score)
            compliance: Compliance check results
            workout_plan: Planned workout description
            recommendation: AI-generated recommendation
            completed: Whether the workout was completed
        
        Returns:
            dict: The created entry with timestamp and ID
        """
        history = self._load_history()
        
        # Initialize user if not exists
        if user_id not in history["users"]:
            history["users"][user_id] = {
                "entries": [],
                "created_at": datetime.now().isoformat(),
                "total_workouts": 0,
                "completed_workouts": 0
            }
        
        # Create new entry
        entry = {
            "id": len(history["users"][user_id]["entries"]) + 1,
            "timestamp": datetime.now().isoformat(),
            "biometrics": biometrics,
            "compliance": {
                "status": compliance.get("status"),
                "severity_score": compliance.get("severity_score", 0),
                "reasons": compliance.get("reasons", [])
            },
            "workout_plan": workout_plan,
            "recommendation_preview": recommendation[:200] + "...",
            "completed": completed,
            "metadata": {
                "day_of_week": datetime.now().strftime("%A"),
                "week_number": datetime.now().isocalendar()[1]
            }
        }
        
        # Add entry
        history["users"][user_id]["entries"].append(entry)
        
        # Update stats
        history["users"][user_id]["total_workouts"] += 1
        if completed:
            history["users"][user_id]["completed_workouts"] += 1
        
        self._save_history(history)
        return entry

    @track
    def get_user_history(
        self, 
        user_id: str, 
        limit: Optional[int] = None,
        days: Optional[int] = None
    ) -> List[dict]:
        """
        Get user's biometric history.
        
        Args:
            user_id: User identifier
            limit: Maximum number of entries to return
            days: Only return entries from last N days
        
        Returns:
            List of historical entries
        """
        history = self._load_history()
        
        if user_id not in history["users"]:
            return []
        
        entries = history["users"][user_id]["entries"]
        
        # Filter by date if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            entries = [
                e for e in entries 
                if datetime.fromisoformat(e["timestamp"]) > cutoff_date
            ]
        
        # Apply limit
        if limit:
            entries = entries[-limit:]
        
        return entries

    @track
    def get_trends(self, user_id: str, days: int = 30) -> dict:
        """
        Analyze biometric trends over time.
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
        
        Returns:
            dict: Trend analysis including averages, trends, and insights
        """
        entries = self.get_user_history(user_id, days=days)
        
        if not entries:
            return {
                "error": "No data available for trend analysis",
                "user_id": user_id,
                "days_analyzed": days
            }
        
        # Calculate averages
        sleep_values = [e["biometrics"]["sleep_hours"] for e in entries]
        hr_values = [e["biometrics"]["resting_hr"] for e in entries]
        recovery_values = [e["biometrics"]["recovery_score"] for e in entries]
        
        # Status distribution
        status_counts = {}
        for e in entries:
            status = e["compliance"]["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate trends (comparing first half vs second half)
        mid = len(entries) // 2
        if mid > 0:
            sleep_trend = self._calculate_trend(
                sleep_values[:mid], 
                sleep_values[mid:]
            )
            hr_trend = self._calculate_trend(
                hr_values[:mid], 
                hr_values[mid:]
            )
            recovery_trend = self._calculate_trend(
                recovery_values[:mid], 
                recovery_values[mid:]
            )
        else:
            sleep_trend = hr_trend = recovery_trend = "insufficient_data"
        
        return {
            "user_id": user_id,
            "period": f"Last {days} days",
            "total_entries": len(entries),
            "averages": {
                "sleep_hours": round(sum(sleep_values) / len(sleep_values), 1),
                "resting_hr": round(sum(hr_values) / len(hr_values)),
                "recovery_score": round(sum(recovery_values) / len(recovery_values))
            },
            "trends": {
                "sleep": sleep_trend,
                "heart_rate": hr_trend,
                "recovery": recovery_trend
            },
            "compliance_distribution": status_counts,
            "insights": self._generate_insights(
                sleep_values, 
                hr_values, 
                recovery_values, 
                status_counts
            )
        }

    def _calculate_trend(self, first_half: List[float], second_half: List[float]) -> str:
        """Calculate if metric is improving, declining, or stable."""
        if not first_half or not second_half:
            return "insufficient_data"
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        change_pct = ((avg_second - avg_first) / avg_first) * 100
        
        if change_pct > 5:
            return "improving"
        elif change_pct < -5:
            return "declining"
        else:
            return "stable"

    def _generate_insights(
        self, 
        sleep: List[float], 
        hr: List[int], 
        recovery: List[int],
        status_counts: dict
    ) -> List[str]:
        """Generate actionable insights from historical data."""
        insights = []
        
        # Sleep insights
        avg_sleep = sum(sleep) / len(sleep)
        if avg_sleep < 7:
            insights.append(
                f"⚠️ Your average sleep ({avg_sleep:.1f}h) is below optimal. "
                f"Prioritize 7-8 hours for better recovery."
            )
        elif avg_sleep >= 8:
            insights.append(
                f"✅ Excellent sleep average ({avg_sleep:.1f}h). Keep it up!"
            )
        
        # Heart rate insights
        avg_hr = sum(hr) / len(hr)
        if avg_hr > 70:
            insights.append(
                f"⚠️ Your average resting HR ({avg_hr:.0f} bpm) is elevated. "
                f"Consider more recovery days or stress management."
            )
        elif avg_hr < 60:
            insights.append(
                f"✅ Great cardiovascular fitness (avg HR: {avg_hr:.0f} bpm)!"
            )
        
        # Compliance insights
        total = sum(status_counts.values())
        critical_pct = (status_counts.get("Critical", 0) / total) * 100
        optimal_pct = (status_counts.get("Optimal", 0) / total) * 100
        
        if critical_pct > 20:
            insights.append(
                f"🚨 {critical_pct:.0f}% of your sessions were 'Critical' status. "
                f"Consider reducing training volume or intensity."
            )
        
        if optimal_pct > 70:
            insights.append(
                f"🎯 {optimal_pct:.0f}% of sessions at 'Optimal' status. "
                f"Your recovery strategy is working well!"
            )
        
        # Recovery score insights
        avg_recovery = sum(recovery) / len(recovery)
        if avg_recovery < 60:
            insights.append(
                f"⚠️ Low average recovery score ({avg_recovery:.0f}/100). "
                f"Focus on sleep quality and stress reduction."
            )
        
        return insights if insights else ["📊 Keep logging data for personalized insights!"]

    @track
    def get_stats(self, user_id: str) -> dict:
        """
        Get user statistics and achievements.
        
        Args:
            user_id: User identifier
        
        Returns:
            dict: User statistics
        """
        history = self._load_history()
        
        if user_id not in history["users"]:
            return {
                "user_id": user_id,
                "total_workouts": 0,
                "completed_workouts": 0,
                "completion_rate": 0,
                "message": "No data yet - start logging your workouts!"
            }
        
        user_data = history["users"][user_id]
        total = user_data["total_workouts"]
        completed = user_data["completed_workouts"]
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            "user_id": user_id,
            "total_workouts": total,
            "completed_workouts": completed,
            "completion_rate": round(completion_rate, 1),
            "member_since": user_data["created_at"],
            "total_entries": len(user_data["entries"])
        }

    @track
    def update_workout_completion(self, user_id: str, entry_id: int, completed: bool):
        """
        Update whether a workout was completed.
        
        Args:
            user_id: User identifier
            entry_id: Entry ID to update
            completed: Completion status
        """
        history = self._load_history()
        
        if user_id not in history["users"]:
            raise ValueError(f"User {user_id} not found")
        
        entries = history["users"][user_id]["entries"]
        
        # Find and update entry
        for entry in entries:
            if entry["id"] == entry_id:
                old_status = entry["completed"]
                entry["completed"] = completed
                entry["completed_at"] = datetime.now().isoformat()
                
                # Update stats
                if completed and not old_status:
                    history["users"][user_id]["completed_workouts"] += 1
                elif not completed and old_status:
                    history["users"][user_id]["completed_workouts"] -= 1
                
                self._save_history(history)
                return entry
        
        raise ValueError(f"Entry {entry_id} not found for user {user_id}")


# Singleton instance
_history_manager = None

def get_history_manager() -> HistoryManager:
    """Get or create the singleton HistoryManager instance."""
    global _history_manager
    if _history_manager is None:
        _history_manager = HistoryManager()
    return _history_manager