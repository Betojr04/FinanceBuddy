import React, { useState, useEffect, useCallback } from "react";
import { usePlaidLink } from "react-plaid-link";

const PlaidLinkButton = () => {
  const [linkToken, setLinkToken] = useState(null);

  // Fetch Link Token from Backend
  useEffect(() => {
    const fetchLinkToken = async () => {
      const response = await fetch("/create_link_token", { method: "POST" });
      const data = await response.json();
      setLinkToken(data.link_token);
    };
    fetchLinkToken();
  }, []);

  const onSuccess = useCallback((publicToken, metadata) => {
    // Send the publicToken to your app server
    // e.g., POST to your '/exchange_public_token' endpoint
  }, []);

  const config = {
    token: linkToken,
    onSuccess,
    // ...other configurations
  };

  const { open, ready } = usePlaidLink(config);

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect a Bank Account
    </button>
  );
};

export default PlaidLinkButton;
