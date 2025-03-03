import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Pagination, EffectFade } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/effect-fade"; 
import Button from "./Button";
import { Ticket } from "lucide-react";

const images = ["/image1.jpg", "/image2.jpg", "/image3.jpg", "/image4.jpg", "/image5.jpg"];

const About = () => {
  return (
    <section className="relative w-full h-[90vh] md:h-[85vh] lg:h-[80vh] rounded-lg overflow-hidden bg-[#cec7bb]">
      <Swiper
        modules={[Autoplay, Pagination, EffectFade]}
        slidesPerView={1}
        autoplay={{ delay: 3000, disableOnInteraction: false }}
        loop={true}
        effect="fade"
        speed={1000}
        allowTouchMove={false}
        pagination={{ clickable: true }}
        className="absolute inset-0 w-full h-full"
      >
        {images.map((img, index) => (
          <SwiperSlide key={index}>
            <div className="relative w-full h-full">
              {/* Background Image */}
              <img
                src={img}
                alt={`Slide ${index + 1}`}
                className="absolute inset-0 w-full h-full object-cover"
              />
              {/* Dark Overlay */}
              <div className="absolute inset-0 bg-black/40"></div>

              {/* Centered Content */}
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-6">
                <h1 className="text-4xl md:text-5xl font-bold text-white drop-shadow-md">
                  Discover the Beauty of CSMVS
                </h1>
                <p className="mt-3 max-w-lg text-gray-300 text-lg md:text-xl">
                  At the Museum you can spend the day among world-class art objects and can participate in fun-n-learn activities.
                </p>
              </div>

              {/* Book Tickets Button Positioned in Bottom Right */}
              <div className="absolute bottom-6 right-6 md:bottom-10 md:right-10">
                <Button className="bg-white hover:bg-[#a81c1ccd] text-gray-900 px-6 py-3 text-lg md:text-xl flex items-center">
                  <Ticket className="mr-2 h-6 w-6" />
                  Book Tickets
                </Button>
              </div>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
};

export default About;
