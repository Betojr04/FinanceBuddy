import React, { useState } from 'react';
import "../../styles/Login.css";

export const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle the form submission logic
        console.log('Form submitted:', formData);
    };

    return (
        <div className="login-container">
            <main className="login-main">
                <h1>Login to Your Account</h1>
                <p>Welcome back! Log in to access your financial dashboard.</p>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email Address:</label>
                        <input 
                            type="email" 
                            id="email" 
                            name="email" 
                            value={formData.email} 
                            onChange={handleChange} 
                            required 
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password:</label>
                        <input 
                            type="password" 
                            id="password" 
                            name="password" 
                            value={formData.password} 
                            onChange={handleChange} 
                            required 
                        />
                    </div>

                    <button type="submit" className="login-button">Login</button>
                </form>
            </main>
        </div>
    );
};


