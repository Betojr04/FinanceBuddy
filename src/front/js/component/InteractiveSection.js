import React from "react";
import "../../styles/InteractiveSection.css";

export const InteractiveSection = () => {
  return (
    <section className="interactive-section">
      <div className="interactive-item">
        <div className="interactive-overlay"></div>
        <h3>Budget Planner</h3>
        <p>
          Engage with our interactive budget planner for smarter financial
          management.
        </p>
      </div>
      <div className="interactive-item">
        <div className="interactive-overlay"></div>
        <h3>Savings Tracker</h3>
        <p>
          Track your savings in real-time with AI-driven insights and forecasts.
        </p>
      </div>
      <div className="interactive-item">
        <div className="interactive-overlay"></div>
        <h3>Investment Simulator</h3>
        <p>
          Experiment with investment scenarios using our AI-based investment
          simulator.
        </p>
      </div>
      {/* Add more interactive elements as needed */}
    </section>
  );
};
