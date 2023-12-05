import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext"; // Update path as needed

export const Navbar = () => {
  const { store, actions } = useContext(Context);
  const isLoggedIn = store.token || localStorage.getItem("token");
  const navigate = useNavigate();

  const handleLogout = () => {
    actions.logoutUser(); // Implement this action in your Flux store
    navigate("/"); // Redirect to home page after logout
  };

  return (
    <nav className="navbar navbar-light bg-light">
      <div className="container">
        <Link to="/">
          <span className="navbar-brand mb-0 h1">FinanceBuddy</span>
        </Link>
        <div className="ml-auto">
          {isLoggedIn ? (
            <>
              <Link to="/private">
                <button className="btn btn-primary">Dashboard</button>
              </Link>
              <button onClick={handleLogout} className="btn btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/register">
                <button className="btn btn-primary">Register</button>
              </Link>
              <Link to="/login">
                <button className="btn btn-primary">Login</button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};
