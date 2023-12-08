import React from "react";
import "../../styles/LiabilitiesCard.css";

export const LiabilitiesCard = ({ liabilities }) => {
  return (
    <div className="liabilities-card">
      <h3>Liabilities</h3>
      <ul>
        {liabilities.map((liability, index) => (
          <li key={index}>
            <p>{liability.type}</p>
            <p>${liability.amount.toFixed(2)}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};
