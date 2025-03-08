import { Link } from 'react-router-dom';
import { SiMusescore } from "react-icons/si";

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="nav-brand">
                <Link to="/">
                    <SiMusescore className='nav-icon'/>
                    <span>MuseBot</span>
                </Link>
            </div>
            <div className="nav-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/chat" className="book-tickets-link">Book Tickets
                </Link>
            </div>
        </nav>
    );
};

export default Navbar; 