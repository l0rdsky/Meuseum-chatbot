import React, { useState } from "react";
import Navbar from "./ui/Navbar";
import About from "./ui/About";
import InfoSection from "./ui/InfoSection";
import PopupCard from "./ui/PopupCard";
import HighlightCards from "./ui/HighlightCards";

export default function HomePage() {
  const [popupContent, setPopupContent] = useState(null);
  const [language, setLanguage] = useState("English"); // State for language selection

  const handleOpenPopup = (content) => {
    setPopupContent(content);
  };

  const handleClosePopup = () => {
    setPopupContent(null);
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#cec7bb]">
      {/* Pass setLanguage and language state to Navbar */}
      <Navbar language={language} setLanguage={setLanguage} />  
      
      <main className="flex-1">
        <About language={language} />
        <InfoSection onItemClick={handleOpenPopup} language={language} />
        <HighlightCards language={language} />
      </main>

      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t border-gray-300 bg-[#cec7bb]">
        <p className="text-xs text-gray-700">© 2023 Museum of Art. All rights reserved.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <a className="text-xs hover:underline underline-offset-4 text-gray-700" href="#">
            About Us
          </a>
          <a className="text-xs hover:underline underline-offset-4 text-gray-700" href="#">
            Contact
          </a>
        </nav>
      </footer>

      {popupContent && <PopupCard content={popupContent} onClose={handleClosePopup} />}
    </div>
  );
}
