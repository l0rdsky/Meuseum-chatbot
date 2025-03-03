import React from "react";

const InfoSection = ({ onItemClick }) => {
  const options = [
    {
      title: "Museum History",
      description:
        "The Chhatrapati Shivaji Maharaj Vastu Sangrahalaya (CSMVS) in Mumbai, formerly known as the Prince of Wales Museum, was established in 1922 to commemorate the visit of Prince of Wales (later King Edward VIII) to India. Designed by architect George Wittet, the museum showcases Indo-Saracenic architecture and houses a vast collection of art, archaeology, and natural history artifacts. Over the years, it has grown into one of India's premier museums, featuring rare sculptures, paintings, textiles, and decorative arts. The museum was renamed in 1998 to honor Chhatrapati Shivaji Maharaj. Today, it remains a center for cultural and historical learning.",
    },
    {
      title: "Visiting Hours",
      description:
        "Monday to Sunday: 10:15 AM to 6:00 PM.\n\nThe museum is closed on the following days:\n- January 26 – Republic Day\n- May 1 – Maharashtra Day\n- August 15 – Independence Day\n- October 2 – Gandhi Jayanti",
    },
  ];

  return (
    <section className="bg-[#cec7bb] flex items-center justify-center py-12 px-4 sm:px-8">
      <div className="max-w-4xl text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">Museum Information</h2>
        <div className="flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
          {options.map((item, index) => (
            <button
              key={index}
              onClick={() => onItemClick(item)}
              className="bg-white px-6 py-4 sm:py-3 rounded-lg shadow-md text-gray-900 text-lg sm:text-xl hover:bg-[#a81c1ccd] hover:text-white transition"
            >
              {item.title}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
};

export default InfoSection;
