import React, { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const LoginRedirect = () => {
  const { actions } = useContext(Context);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      actions.setToken(token);
      navigate("/private"); // redirect to private view
    }
  }, []);

  return null; // renders nothing
};
