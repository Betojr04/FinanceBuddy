import React from "react";
import { Link } from "react-router-dom";
import "../../styles/HeroSection.css";

export const HeroSection = () => {
  return (
    <div className="hero-container">
      <h1>Welcome to FinanceBuddy</h1>
      <p>Your personal finance tracker</p>
      <Link to="/register">
        <button className="hero-button">Get Started</button>
      </Link>
    </div>
  );
};
