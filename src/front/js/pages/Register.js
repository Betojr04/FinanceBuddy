import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/Register.css";

export const Register = () => {
  const { actions } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleClick = async (e) => {
    e.preventDefault(); // this prevents a reload every time
    await actions.registerUser(email, password); //this is calling the registerUser function from flux
  };

  return (
    <div className="register-container">
      <main className="register-main">
        <h1>Create Your Account</h1>
        <p>
          Join us and start managing your finances smarter with AI insights.
        </p>

        <form>
          {/* <div className="form-group">
                        <label htmlFor="name">Full Name:</label>
                        <input 
                            type="text" 
                            id="name" 
                            name="name" 
                            required 
                        />
                    </div> */}

          <div className="form-group">
            <label htmlFor="email">Email Address:</label>
            <input
              type="email"
              id="email"
              name="example"
              placeholder="email@example.com"
              value={email}
              onChange={(e) => {
                console.log("Email:", e.target.value);
                setEmail(e.target.value);
              }}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="password"
              value={password}
              onChange={(e) => {
                console.log("Password:", e.target.value);
                setPassword(e.target.value);
              }}
              required
            />
          </div>

          <button type="submit" onClick={handleClick} className="submit-button">
            Register
          </button>
        </form>
      </main>
    </div>
  );
};
