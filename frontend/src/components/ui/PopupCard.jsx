import React from "react";
import { X } from "lucide-react";

const PopupCard = ({ content, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50 p-4">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full text-center relative">
        <button onClick={onClose} className="absolute top-3 right-3 text-gray-600 hover:text-gray-900">
          <X className="w-6 h-6" />
        </button>
        <h2 className="text-xl font-semibold mb-2">{content.title}</h2>
        <p className="text-gray-600">{content.description}</p>
      </div>
    </div>
  );
};

export default PopupCard;
