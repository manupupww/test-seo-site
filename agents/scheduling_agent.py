from tools.scheduling_tool import SchedulingTool

class SchedulingAgent:
    def __init__(self):
        self.tool = SchedulingTool()

    def generate_eta_content(self):
        """Generate ETA and scheduling content for website"""
        content = self.tool.generate_eta_content()
        return content

    def create_scheduling_page(self):
        """Create a scheduling page with ETA features"""
        eta_content = self.generate_eta_content()

        page_content = f"""---
layout: page
title: "Service Scheduling & ETA"
description: "Book your junk removal service and get instant ETA estimates in Vilnius"
---

# Service Scheduling & Real-Time ETA

{eta_content}

## Book Your Service

<div class="booking-form">
    <form id="bookingForm">
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" required>
        </div>
        <div class="mb-3">
            <label for="phone" class="form-label">Phone</label>
            <input type="tel" class="form-control" id="phone" required>
        </div>
        <div class="mb-3">
            <label for="location" class="form-label">Location in Vilnius</label>
            <input type="text" class="form-control" id="location" placeholder="e.g., Vilnius center, suburb" required>
        </div>
        <div class="mb-3">
            <label for="service" class="form-label">Service Type</label>
            <select class="form-control" id="service">
                <option>Junk Removal</option>
                <option>Furniture Removal</option>
                <option>Appliance Disposal</option>
                <option>Office Cleanout</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Get ETA & Book</button>
    </form>
</div>

<div id="etaResult" class="mt-3" style="display: none;">
    <div class="alert alert-success">
        <h5>Your ETA:</h5>
        <p id="etaText"></p>
    </div>
</div>

<script>
document.getElementById('bookingForm').addEventListener('submit', function(e) {{
    e.preventDefault();
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const location = document.getElementById('location').value;
    const service = document.getElementById('service').value;

    // Mock ETA calculation (in real implementation, call backend API)
    const etaMinutes = Math.floor(Math.random() * 60) + 30;
    const etaTime = new Date(Date.now() + etaMinutes * 60000).toLocaleTimeString();

    document.getElementById('etaText').innerHTML = `<strong>${{etaMinutes}} minutes</strong> - Estimated arrival: ${{etaTime}}<br>We'll call you at ${{phone}} to confirm.`;
    document.getElementById('etaResult').style.display = 'block';

    // In real implementation, send data to backend for processing
    console.log('Booking:', {{name, phone, location, service}});
}});
</script>
"""
        return page_content

# Usage: agent = SchedulingAgent(); content = agent.generate_eta_content(); page = agent.create_scheduling_page()