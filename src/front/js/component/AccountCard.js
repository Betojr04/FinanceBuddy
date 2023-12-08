import React from "react";
import "../../styles/AccountCard.css";

export const AccountCard = ({ account }) => {
  return (
    <div className="account-card">
      <div className="account-info">
        <h3>{account.name}</h3>
        <p>Type: {account.type}</p>
      </div>
      <div className="account-balance">
        <p>Balance: ${account.balances.current.toFixed(2)}</p>
        <p>Available: ${account.balances.available.toFixed(2)}</p>
      </div>
    </div>
  );
};
