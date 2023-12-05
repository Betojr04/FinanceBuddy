import React, { useState, useContext } from "react";
import { Context } from "../store/appContext.js";
import { useNavigate } from "react-router-dom";

import "../../styles/Login.css";

export const Login = () => {
  const { actions, store } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await actions.loginUser(email, password);

    if (store.token) {
      navigate("/private"); // Redirect to the dashboard
    }
  };

  return (
    <div className="login-container">
      <main className="login-main">
        <h1>Login to Your Account</h1>
        <p>Welcome back! Log in to access your financial dashboard.</p>

        {store.loginError && (
          <p className="error-message">{store.loginError}</p>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-button">
            Login
          </button>
        </form>
      </main>
    </div>
  );
};
