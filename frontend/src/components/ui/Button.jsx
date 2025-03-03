import React from "react";

const Button = ({ children, variant = "default", className = "", ...props }) => {
  const baseStyles = "px-4 py-2 rounded text-sm font-medium transition";
  
  const variants = {
    default: "bg-blue-600 text-white",
    outline: "border border-gray-500 text-gray-700 hover:bg-gray-700 hover:text-white",
  };

  return (
    <button className={`${baseStyles} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
};

export default Button;
