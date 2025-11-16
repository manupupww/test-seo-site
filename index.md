---
layout: default
title: "Expert Junk Removal Services | Quick Junk Removal"
description: "Professional junk removal and disposal services in Vilnius. Eco-friendly waste management, fast service, 5-star customer satisfaction."
---

<div class="hero-section bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold">Expert Junk Removal Services</h1>
                <p class="lead">Professional junk removal and eco-friendly disposal in Vilnius. Fast, reliable, and affordable service.</p>
                <a href="#contact" class="btn btn-light btn-lg me-3">Get Free Quote</a>
                <a href="#services" class="btn btn-outline-light btn-lg">Our Services</a>
            </div>
            <div class="col-lg-6">
                <img src="/images/junk-removal-hero.jpg" alt="Junk removal service" class="img-fluid rounded" onerror="this.src='https://via.placeholder.com/600x400?text=Junk+Removal+Service'">
            </div>
        </div>
    </div>
</div>

<section id="services" class="py-5">
    <div class="container">
        <h2 class="text-center mb-5">Our Services</h2>
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <h5 class="card-title">Residential Cleanouts</h5>
                        <p class="card-text">Complete home cleanouts, garage clearing, and household junk removal.</p>
                        <p class="text-primary fw-bold">From €50</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <h5 class="card-title">Office Cleanouts</h5>
                        <p class="card-text">Commercial space clearing, office furniture removal, and document disposal.</p>
                        <p class="text-primary fw-bold">From €100</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body text-center">
                        <h5 class="card-title">Eco-Friendly Disposal</h5>
                        <p class="card-text">Environmentally responsible waste disposal and recycling services.</p>
                        <p class="text-primary fw-bold">Included</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="bg-light py-5">
    <div class="container text-center">
        <h2>Why Choose Us?</h2>
        <div class="row mt-4">
            <div class="col-md-4">
                <h4>Fast Service</h4>
                <p>Same-day service available for most requests</p>
            </div>
            <div class="col-md-4">
                <h4>Eco-Friendly</h4>
                <p>We recycle up to 80% of collected materials</p>
            </div>
            <div class="col-md-4">
                <h4>Competitive Pricing</h4>
                <p>Transparent pricing with no hidden fees</p>
            </div>
        </div>
    </div>
</section>

<section id="contact" class="py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <h2 class="text-center mb-4">Get Your Free Quote</h2>
                <div class="card shadow">
                    <div class="card-body p-4">
                        <form id="quoteForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="name" class="form-label">Name *</label>
                                    <input type="text" class="form-control" id="name" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="phone" class="form-label">Phone *</label>
                                    <input type="tel" class="form-control" id="phone" required>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email">
                            </div>
                            <div class="mb-3">
                                <label for="service" class="form-label">Service Type *</label>
                                <select class="form-control" id="service" required>
                                    <option value="">Select service</option>
                                    <option>Residential Cleanout</option>
                                    <option>Office Cleanout</option>
                                    <option>Yard Waste Removal</option>
                                    <option>Furniture Removal</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="message" class="form-label">Description</label>
                                <textarea class="form-control" id="message" rows="3" placeholder="Describe what needs to be removed..."></textarea>
                            </div>
                            <div class="text-center">
                                <button type="submit" class="btn btn-primary btn-lg">Get Free Quote</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
document.getElementById('quoteForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Thank you! We will contact you within 1 hour with your free quote.');
    this.reset();
});
</script>