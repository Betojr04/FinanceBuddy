import React from "react";
import { Context } from "../store/appContext";
import { usePlaidLink } from "react-plaid-link";
import { Link } from "react-router-dom";
import { PlaidLinkButton } from "../component/PlaidLinkButton";

export const PrivateView = () => {
  return (
    <main>
      <h3>this is the users private view</h3>
      <PlaidLinkButton />
    </main>
  );
};
