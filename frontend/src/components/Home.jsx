import React from 'react';
import { useNavigate } from 'react-router-dom';
// Import images
import museumInterior from '../assets/images/museum-interior.jpg';
import ancientArtifacts from '../assets/images/ancient-artifacts.jpg';
import artGallery from '../assets/images/art-gallery.jpg';
import culturalEvents from '../assets/images/cultural-events.jpg';

const Home = () => {
    const navigate = useNavigate();

    return (
        <>
            <div className="hero-section">
                <h1>National Museum of India</h1>
                <p>Discover India's Rich Cultural Heritage</p>
                <button className="book-ticket-btn" onClick={() => navigate('/chat')}>
                    Book Tickets Now
                </button>
            </div>

            <section className="about-section">
                <h2>About the Museum</h2>
                <div className="about-content">
                    <div className="about-text">
                        <p>The National Museum of India, located in the heart of New Delhi, houses over 200,000 works of art spanning over 5,000 years of cultural heritage.</p>
                        <p>Our collections include ancient artifacts, decorative arts, paintings, and manuscripts that showcase India's rich cultural diversity and historical significance.</p>
                    </div>
                    <div className="museum-image">
                        <img src={museumInterior} alt="Museum Interior" />
                    </div>
                </div>
            </section>

            <section className="highlights-section">
                <h2>Museum Highlights</h2>
                <div className="highlights-grid">
                    <div className="highlight-card">
                        <img src={ancientArtifacts} alt="Ancient Artifacts" />
                        <h3>Ancient Artifacts</h3>
                        <p>Explore our collection of ancient artifacts dating back to the Indus Valley Civilization.</p>
                    </div>
                    <div className="highlight-card">
                        <img src={artGallery} alt="Art Gallery" />
                        <h3>Art Gallery</h3>
                        <p>View masterpieces from various Indian art schools and periods.</p>
                    </div>
                    <div className="highlight-card">
                        <img src={culturalEvents} alt="Cultural Events" />
                        <h3>Cultural Events</h3>
                        <p>Participate in regular cultural events and exhibitions.</p>
                    </div>
                </div>
            </section>
        </>
    );
};

export default Home; 