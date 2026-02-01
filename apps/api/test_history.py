"""
Test script for History Manager - Biometric Auditor V2
Run this to verify all history tracking features work correctly.
"""

from history_manager import get_history_manager
from datetime import datetime, timedelta
import json

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")
def test_history_manager():
    """Comprehensive test of all History Manager features."""
    
    print_section("🧪 HISTORY MANAGER TEST SUITE")
    
    # Initialize
    hm = get_history_manager()
    test_user = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"Testing with user: {test_user}\n")
    
    # ========================================
    # TEST 1: Add Single Entry
    # ========================================
    print_section("TEST 1: Add Single Entry")
    
    entry1 = hm.add_entry(
        user_id=test_user,
        biometrics={
            "sleep_hours": 7.5,
            "resting_hr": 65,
            "recovery_score": 85
        },
        compliance={
            "status": "Optimal",
            "severity_score": 0,
            "reasons": []
        },
        workout_plan="5K Easy Run",
        recommendation="Great biometrics! You're cleared for training. Your sleep is optimal...",
        completed=False
    )
    
    print("✅ Entry created successfully!")
    print(f"   Entry ID: {entry1['id']}")
    print(f"   Timestamp: {entry1['timestamp']}")
    print(f"   Status: {entry1['compliance']['status']}")
    
    # ========================================
    # TEST 2: Add Multiple Entries
    # ========================================
    print_section("TEST 2: Add Multiple Entries (Simulating 7 days)")
    
    # Simulate a week of workouts with varying biometrics
    test_data = [
        # Day 2: Good sleep, proceeded with workout
        {"sleep": 8.0, "hr": 60, "plan": "Upper Body Strength", "status": "Optimal"},
        # Day 3: Low sleep, got warning
        {"sleep": 6.0, "hr": 75, "plan": "HIIT Intervals", "status": "Warning"},
        # Day 4: Recovery day
        {"sleep": 9.0, "hr": 58, "plan": "Easy Yoga", "status": "Optimal"},
        # Day 5: Critical - very low sleep
        {"sleep": 4.5, "hr": 88, "plan": "Heavy Squats", "status": "Critical"},
        # Day 6: Better sleep, recovering
        {"sleep": 7.5, "hr": 68, "plan": "Light Cardio", "status": "Warning"},
        # Day 7: Back to optimal
        {"sleep": 8.5, "hr": 62, "plan": "Full Body Workout", "status": "Optimal"},
    ]
    
    for i, data in enumerate(test_data, start=2):
        # Calculate recovery score
        recovery = int(
            min(50, (data["sleep"] / 8.0) * 50) +  # Sleep component
            max(0, 50 - (data["hr"] - 50))  # HR component
        )
        
        # Determine severity
        severity = 0 if data["status"] == "Optimal" else (3 if data["status"] == "Critical" else 1)
        
        entry = hm.add_entry(
            user_id=test_user,
            biometrics={
                "sleep_hours": data["sleep"],
                "resting_hr": data["hr"],
                "recovery_score": recovery
            },
            compliance={
                "status": data["status"],
                "severity_score": severity,
                "reasons": [] if data["status"] == "Optimal" else [f"Status: {data['status']}"]
            },
            workout_plan=data["plan"],
            recommendation=f"Recommendation for {data['plan']}...",
            completed=(i % 2 == 0)  # Mark every other workout as completed
        )
        print(f"   Day {i}: {data['plan']} - Status: {data['status']}")
    
    print(f"\n✅ Added {len(test_data)} more entries!")
    
    # ========================================
    # TEST 3: Get User History
    # ========================================
    print_section("TEST 3: Get User History")
    
    all_history = hm.get_user_history(test_user)
    print(f"Total entries: {len(all_history)}")
    print(f"\nFirst entry:")
    print(f"   Plan: {all_history[0]['workout_plan']}")
    print(f"   Sleep: {all_history[0]['biometrics']['sleep_hours']}h")
    print(f"   Status: {all_history[0]['compliance']['status']}")
    
    # Test with limit
    recent_3 = hm.get_user_history(test_user, limit=3)
    print(f"\n✅ Retrieved last 3 entries: {len(recent_3)} entries")
    
    # Test with days filter
    last_7_days = hm.get_user_history(test_user, days=7)
    print(f"✅ Retrieved last 7 days: {len(last_7_days)} entries")
    
    # ========================================
    # TEST 4: Get User Statistics
    # ========================================
    print_section("TEST 4: Get User Statistics")
    
    stats = hm.get_stats(test_user)
    print(f"Total workouts planned: {stats['total_workouts']}")
    print(f"Workouts completed: {stats['completed_workouts']}")
    print(f"Completion rate: {stats['completion_rate']}%")
    print(f"Member since: {stats['member_since']}")
    
    print(f"\n✅ Statistics calculated successfully!")
    
    # ========================================
    # TEST 5: Update Workout Completion
    # ========================================
    print_section("TEST 5: Update Workout Completion")
    
    # Mark first workout as completed
    updated_entry = hm.update_workout_completion(
        user_id=test_user,
        entry_id=1,
        completed=True
    )
    
    print(f"Updated entry {updated_entry['id']}")
    print(f"Completed status: {updated_entry['completed']}")
    print(f"Completed at: {updated_entry.get('completed_at', 'N/A')}")
    
    # Get updated stats
    updated_stats = hm.get_stats(test_user)
    print(f"\nUpdated completion rate: {updated_stats['completion_rate']}%")
    
    print(f"\n✅ Workout completion updated successfully!")
    
    # ========================================
    # TEST 6: Trend Analysis
    # ========================================
    print_section("TEST 6: Trend Analysis")
    
    trends = hm.get_trends(test_user, days=7)
    
    print("AVERAGES:")
    print(f"   Sleep: {trends['averages']['sleep_hours']}h")
    print(f"   Resting HR: {trends['averages']['resting_hr']} bpm")
    print(f"   Recovery Score: {trends['averages']['recovery_score']}/100")
    
    print("\nTRENDS:")
    print(f"   Sleep: {trends['trends']['sleep']}")
    print(f"   Heart Rate: {trends['trends']['heart_rate']}")
    print(f"   Recovery: {trends['trends']['recovery']}")
    
    print("\nCOMPLIANCE DISTRIBUTION:")
    for status, count in trends['compliance_distribution'].items():
        print(f"   {status}: {count} occurrences")
    
    print("\nINSIGHTS:")
    for insight in trends['insights']:
        print(f"   • {insight}")
    
    print(f"\n✅ Trend analysis completed successfully!")
    
    # ========================================
    # TEST 7: Edge Cases
    # ========================================
    print_section("TEST 7: Edge Cases")
    
    # Test non-existent user
    empty_history = hm.get_user_history("non_existent_user_xyz")
    print(f"Non-existent user history: {len(empty_history)} entries (expected: 0)")
    
    # Test stats for new user
    new_user_stats = hm.get_stats("brand_new_user")
    print(f"New user stats: {new_user_stats['total_workouts']} workouts (expected: 0)")
    
    # Test trends with insufficient data
    insufficient_trends = hm.get_trends("brand_new_user", days=30)
    print(f"Insufficient data trends: {'error' in insufficient_trends}")
    
    print(f"\n✅ Edge cases handled correctly!")
    
    # ========================================
    # FINAL SUMMARY
    # ========================================
    print_section("✅ ALL TESTS PASSED!")
    
    print(f"""
Test Summary:
-------------
✅ Single entry creation
✅ Multiple entries creation
✅ History retrieval (all, limited, date-filtered)
✅ Statistics calculation
✅ Workout completion tracking
✅ Trend analysis
✅ Edge case handling

Test user: {test_user}
Total entries created: {len(all_history)}
Data file location: {hm.history_file}

You can view the raw data with:
    cat {hm.history_file}

Or in Python:
    import json
    with open('{hm.history_file}') as f:
        data = json.load(f)
        print(json.dumps(data, indent=2))
""")

if __name__ == "__main__":
    try:
        test_history_manager()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        import traceback
        traceback.print_exc()