import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { X } from "lucide-react";
import ancientArtifacts from "../assets/images/ancient-artifacts.jpg";
import artGallery from "../assets/images/art-gallery.jpg";
import culturalEvents from "../assets/images/cultural-events.jpg";
import museumInterior from "../assets/images/museum-interior.jpg";
import image1 from "../assets/images/image1.jpg";
import image4 from "../assets/images/image4.jpg";
import image5 from "../assets/images/image5.jpg";


const highlightsData = [
  {
    id: 1,
    title: "Ancient Artifacts",
    img: ancientArtifacts,
    description: "Explore our collection of ancient artifacts dating back to the Indus Valley Civilization.",
    popupInfo: "These artifacts provide insights into early human civilization, tools, sculptures, and writings from ancient India."
  },
  {
    id: 2,
    title: "Art Gallery",
    img: artGallery,
    description: "View masterpieces from various Indian art schools and periods.",
    popupInfo: "The gallery showcases works from renowned Indian artists, including Mughal, Rajput, and contemporary art."
  },
  {
    id: 3,
    title: "Cultural Events",
    img: culturalEvents,
    description: "Participate in regular cultural events and exhibitions.",
    popupInfo: "Our events celebrate India's rich cultural heritage, featuring traditional dance, music, and workshops."
  }
];

const Home = () => {
  const [selectedHighlight, setSelectedHighlight] = useState(null);
  const navigate = useNavigate();

  return (
    <>
      <div className="hero-section">
        <Carousel
          autoPlay
          infiniteLoop
          showThumbs={false}
          showStatus={false}
          interval={2500}
          swipeable={true}
          stopOnHover={false}
          className="carousel-container small-carousel"
        >
          <div className="carousel-slide">
            <img src={image4} alt="Museum Interior" className="carousel-image small-image" />
            <div className="carousel-text">
              <h1>National Museum of India</h1>
              <p>Discover India's Rich Cultural Heritage</p>
            </div>
          </div>
          <div className="carousel-slide">
            <img src={ancientArtifacts} alt="Ancient Artifacts" className="carousel-image small-image" />
            <div className="carousel-text">
              <h1>Ancient Artifacts</h1>
              <p>Explore treasures from India's past</p>
            </div>
          </div>
          <div className="carousel-slide">
            <img src={image1} alt="Art Gallery" className="carousel-image small-image" />
            <div className="carousel-text">
              <h1>Art Gallery</h1>
              <p>Admire stunning artworks from various eras</p>
            </div>
          </div>
          <div className="carousel-slide">
            <img src={image5} alt="Cultural Events" className="carousel-image small-image" />
            <div className="carousel-text">
              <h1>Cultural Events</h1>
              <p>Experience vibrant traditions and celebrations</p>
            </div>
          </div>
        </Carousel>
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
          {highlightsData.map((highlight) => (
            <div
              key={highlight.id}
              className="highlight-card"
              onClick={() => setSelectedHighlight(highlight)}
            >
              <img src={highlight.img} alt={highlight.title} />
              <h3>{highlight.title}</h3>
              <p>{highlight.description}</p>
            </div>
          ))}
        </div>

        {selectedHighlight && (
          <div className="popup-overlay" onClick={() => setSelectedHighlight(null)}>
            <div className="popup-content" onClick={(e) => e.stopPropagation()}>
              <button className="close-btn" onClick={() => setSelectedHighlight(null)}>
                <X className="w-6 h-6" />
              </button>
              <h3>{selectedHighlight.title}</h3>
              <p>{selectedHighlight.popupInfo}</p>
            </div>
          </div>
        )}
      </section>
    </>
  );
};

export default Home;
