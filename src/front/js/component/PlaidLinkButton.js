import React, { useState, useEffect, useCallback, useContext } from "react";
import { usePlaidLink } from "react-plaid-link";
import { Context } from "../store/appContext.js";

export const PlaidLinkButton = () => {
  const { dispatch } = useContext(Context); // Use dispatch from your context
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

        // Dispatch the new state to your context
        dispatch({
          type: "SET_STATE",
          state: {
            accessToken: data.access_token,
            // ...other state updates as necessary
          },
        });
      } catch (error) {
        console.error("Error exchanging public token:", error);
      }
    },
    [dispatch]
  );

  const config = { token: linkToken, onSuccess };

  const { open, ready } = usePlaidLink(config);

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect a Bank Account
    </button>
  );
};
