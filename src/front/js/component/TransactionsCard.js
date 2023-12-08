import React from "react";
import "../../styles/TransactionsCard.css";

export const TransactionsCard = ({ transactions }) => {
  return (
    <div className="transactions-card">
      <h3>Transactions</h3>
      <ul>
        {transactions.map((transaction, index) => (
          <li key={index}>
            <p>{transaction.name}</p>
            <p>${transaction.amount.toFixed(2)}</p>
            <p>{transaction.date}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};
