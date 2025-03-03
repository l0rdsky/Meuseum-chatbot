import React, { useState } from "react";
import Button from "./Button";
import { Ticket, Globe, Landmark, Menu, X } from "lucide-react";

const Navbar = ({ language, setLanguage }) => {
  const [showLanguageDropdown, setShowLanguageDropdown] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="relative bg-[#a81c1c] shadow-md h-16 flex items-center justify-between px-6 md:px-12 transition-all z-50">
      {/* Logo & Title */}
      <div className="flex items-center space-x-3">
        <Landmark className="h-8 w-8 text-white" />
        <h1 className="text-xl md:text-3xl font-bold text-white">
          CSMVS Museum
        </h1>
      </div>

      {/* Mobile Menu Button */}
      <button
        className="md:hidden text-white"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        {menuOpen ? <X className="h-8 w-8" /> : <Menu className="h-8 w-8" />}
      </button>

      {/* Desktop & Mobile Menu */}
      <div
        className={`absolute md:static top-16 left-0 w-full md:w-auto bg-[#a81c1c] md:bg-transparent flex flex-col md:flex-row items-center md:space-x-6 transition-all ${
          menuOpen ? "block" : "hidden md:flex"
        }`}
      >
        {/* Language Dropdown */}
        <div className="relative mt-4 md:mt-0">
          <button
            onClick={() => setShowLanguageDropdown(!showLanguageDropdown)}
            className="p-2 bg-transparent border border-white rounded-lg flex items-center transition-all text-white hover:bg-[#cec7bb] hover:text-[#800000]"
          >
            <Globe className="h-6 w-6 text-white mr-2" />
            <span className="font-medium">{language}</span>
          </button>

          {showLanguageDropdown && (
            <div className="absolute top-full left-0 mt-2 bg-white text-black rounded-lg shadow-lg w-36 p-2 z-50">
              {["English", "Hindi"].map((lang) => (
                <div
                  key={lang}
                  className={`p-2 cursor-pointer hover:bg-gray-200 rounded ${
                    language === lang ? "font-bold text-[#800000]" : ""
                  }`}
                  onClick={() => {
                    setLanguage(lang); // Update language globally
                    setShowLanguageDropdown(false);
                  }}
                >
                  {lang}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Book Tickets Button */}
        <Button className="mt-4 md:mt-0 bg-transparent border border-white text-white px-5 py-2 text-lg flex items-center shadow-md transition-all hover:bg-[#cec7bb] hover:text-[#800000]">
          <Ticket className="mr-2 h-5 w-5 text-white transition-all group-hover:text-[#800000]" />
          Book Tickets
        </Button>
      </div>
    </header>
  );
};

export default Navbar;
