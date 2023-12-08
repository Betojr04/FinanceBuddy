import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { PlaidLinkButton } from "../component/PlaidLinkButton";
import { AccountCard } from "../component/AccountCard";
import "../../styles/PrivateView.css";

export const PrivateView = () => {
  const { store } = useContext(Context);

  return (
    <main className="dashboard">
      <h3>My Dashboard</h3>
      {!store.accessToken && (
        <div className="connect-prompt">
          <p>No account information connected yet.</p>
          <PlaidLinkButton />
        </div>
      )}
      {store.accounts && store.accounts.length > 0
        ? store.accounts.map((account) => (
            <AccountCard key={account.account_id} account={account} />
          ))
        : store.accessToken && <p>Loading your account information...</p>}
    </main>
  );
};
