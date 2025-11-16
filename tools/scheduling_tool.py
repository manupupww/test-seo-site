import os
import requests
from datetime import datetime, timedelta
import json

class SchedulingTool:
    def __init__(self, api_key=None):
        self.api_key = api_key  # For future integrations like Google Maps API

    def calculate_eta(self, customer_location, service_location="Vilnius", current_time=None):
        """Calculate estimated time of arrival based on location and time"""
        if current_time is None:
            current_time = datetime.now()

        # Mock ETA calculation (in real implementation, use Google Maps API)
        base_eta = 60  # 60 minutes base

        # Adjust for time of day (rush hours)
        hour = current_time.hour
        if 7 <= hour <= 9 or 16 <= hour <= 18:  # Rush hours
            base_eta += 20

        # Adjust for day of week
        if current_time.weekday() >= 5:  # Weekend
            base_eta -= 10

        # Adjust for location (mock distance factor)
        if "center" in customer_location.lower():
            base_eta += 15
        elif "suburb" in customer_location.lower():
            base_eta += 30

        eta_datetime = current_time + timedelta(minutes=base_eta)

        return {
            "eta_minutes": base_eta,
            "eta_datetime": eta_datetime.isoformat(),
            "estimated_arrival": eta_datetime.strftime("%H:%M"),
            "confidence": "high" if base_eta < 90 else "medium"
        }

    def schedule_service(self, customer_info, service_type="junk removal", preferred_time=None):
        """Schedule a service and provide ETA"""
        eta_info = self.calculate_eta(customer_info.get("location", "Vilnius"))

        booking = {
            "booking_id": f"booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "customer": customer_info,
            "service_type": service_type,
            "scheduled_time": preferred_time or eta_info["eta_datetime"],
            "eta_info": eta_info,
            "status": "confirmed",
            "confirmation_message": f"Your {service_type} service is scheduled. Estimated arrival: {eta_info['estimated_arrival']} ({eta_info['eta_minutes']} minutes from now)."
        }

        # Save booking (mock - in real app, save to database)
        self._save_booking(booking)

        return booking

    def generate_eta_content(self):
        """Generate website content about ETA and scheduling"""
        content = """## Fast & Reliable Service Scheduling

### Get Your ETA Instantly

Our advanced scheduling system provides real-time ETAs based on:
- Current traffic conditions
- Your location in Vilnius
- Time of day and day of week
- Service type and complexity

### How Our ETA System Works

1. **Book Online**: Fill out our simple booking form
2. **Get Instant ETA**: Receive your estimated arrival time immediately
3. **Real-time Updates**: Get SMS updates if conditions change
4. **Flexible Scheduling**: Choose your preferred time slots

### Average Response Times

- **Weekday Mornings (8-10 AM)**: 45-60 minutes
- **Weekday Evenings (4-6 PM)**: 60-90 minutes
- **Weekends**: 30-45 minutes
- **Emergency Services**: 15-30 minutes

### Book Your Service Now

Call +370-XXX-XXXX or use our online booking form to get your personalized ETA today!

*All ETAs are estimates and may vary based on traffic and service requirements.*
"""
        return content

    def _save_booking(self, booking):
        """Mock save booking to file"""
        try:
            with open("bookings.json", "a") as f:
                json.dump(booking, f)
                f.write("\n")
        except:
            pass  # Mock, ignore errors

# Usage: tool = SchedulingTool(); eta = tool.calculate_eta("Vilnius center"); booking = tool.schedule_service({"name": "John", "location": "Vilnius"})