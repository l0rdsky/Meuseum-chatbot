import React from "react";

const exhibits = [
  {
    title: "India's Early Picture Books",
    description: "A stunning collection of Van Gogh's famous sunflower paintings.",
    image: "/unique1.webp",
  },
  {
    title: "Chinese Snuff Bottles",
    description: "Explore the rich history of ancient Egypt through our artifacts.",
    image: "/unique2.webp",
  },
  {
    title: "A 10-yard sari that celebrates the best of Indian textiles",
    description: "Contemporary sculptures that challenge and inspire.",
    image: "/unique3.png",
  },
  {
    title: "Beginnings of the graphic novel in India",
    description: "Contemporary sculptures that challenge and inspire.",
    image: "/unique4.webp",
  },
  {
    title: "The Indo-Saracenic style",
    description: "Contemporary sculptures that challenge and inspire.",
    image: "/unique5.webp",
  },
];

const HighlightCards = () => {
  return (
    <section className="w-full py-4 md:py-8 bg-[#cec7bb]"> {/* Reduced top padding */}
      <div className="container px-4 md:px-6">
        <h2 className="text-2xl md:text-4xl font-bold tracking-tight text-center mb-6">
          Some Unique Highlights of CSMVS
        </h2>
        <div className="flex gap-6 overflow-x-auto hide-scrollbar">
          {exhibits.map((exhibit, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center text-center transition-all duration-300 hover:scale-105 w-64 h-80 flex-shrink-0"
            >
              <img
                src={exhibit.image}
                alt={exhibit.title}
                className="w-52 h-40 object-cover rounded-lg mb-4"
              />
              <h3 className="text-lg font-semibold">{exhibit.title}</h3>
              <p className="text-gray-600 text-sm">{exhibit.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HighlightCards;
