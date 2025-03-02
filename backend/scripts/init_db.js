db.museums.insertOne({
    name: "National Museum of India",
    description: "The National Museum of India, established in 1949, houses over 200,000 works of art representing 5,000 years of Indian heritage. Our collections span ancient artifacts, decorative arts, paintings, and manuscripts.",
    opening_hours: "Tuesday to Sunday: 10:00 AM - 6:00 PM\nClosed on Mondays and National Holidays",
    location: "Janpath Road, Central Secretariat, New Delhi, Delhi 110011",
    contact: "Phone: +91-11-23019272\nEmail: info@nationalmuseumindia.gov.in",
    ticket_prices: {
        adult: 500,
        student: 250,
        child: 0
    }
}); 