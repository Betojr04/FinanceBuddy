import React, { useState, useEffect, useCallback, useContext } from "react";
import { usePlaidLink } from "react-plaid-link";
import { Context } from "../store/appContext.js";
import "../../styles/PlaidLinkButton.css";

export const PlaidLinkButton = () => {
  const { actions } = useContext(Context);
  const [linkToken, setLinkToken] = useState(null);

  // Fetch Link Token from Backend
  useEffect(() => {
    const fetchLinkToken = async () => {
      try {
        const response = await fetch(
          `${process.env.BACKEND_URL}api/create_link_token`,
          { method: "POST" }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setLinkToken(data.link_token);
      } catch (error) {
        console.error("Error fetching link token:", error);
      }
    };

    fetchLinkToken();
  }, []);

  const onSuccess = useCallback(
    async (publicToken, metadata) => {
      try {
        const response = await fetch(
          `${process.env.BACKEND_URL}api/exchange_public_token`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ public_token: publicToken }),
          }
        );

        if (!response.ok) {
          throw new Error("Exchange token failed");
        }

        const data = await response.json();
        console.log("Access token:", data.access_token);

        // Use setAccessToken action from your flux actions
        actions.setAccessToken(data.access_token);
      } catch (error) {
        console.error("Error exchanging public token:", error);
      }
    },
    [actions]
  );

  const config = { token: linkToken, onSuccess };

  const { open, ready } = usePlaidLink(config);

  return (
    <button
      className="plaid-link-button"
      onClick={() => open()}
      disabled={!ready}
    >
      Connect a Bank Account
    </button>
  );
};
