import React from 'react';
import { Link } from 'react-router-dom';
import { MdMuseum } from 'react-icons/md';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="nav-brand">
                <Link to="/">
                    <MdMuseum className="nav-icon" />
                    <span>National Museum</span>
                </Link>
            </div>
            <div className="nav-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/chat" className="book-tickets-link">Book Tickets</Link>
            </div>
        </nav>
    );
};

export default Navbar; 