import React from "react";
import "../../styles/FeatureSection.css";

export const FeatureSection = () => {
  return (
    <section className="feature-section">
      <div className="feature-item" id="feature-ai">
        <h2>AI-Driven Insights</h2>
        <p>
          Unlock personalized financial advice with our advanced AI algorithms.
        </p>
      </div>
      <div className="feature-item" id="feature-security">
        <h2>Robust Security</h2>
        <p>Experience top-tier security protecting your financial data.</p>
      </div>
      <div className="feature-item" id="feature-reports">
        <h2>Visual Reports</h2>
        <p>Engage with intuitive, easy-to-understand financial reports.</p>
      </div>
      <div className="feature-item" id="feature-education">
        <h2>Financial Education</h2>
        <p>Empower your financial decisions with our educational tools.</p>
      </div>
    </section>
  );
};
