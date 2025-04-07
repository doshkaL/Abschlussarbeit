import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./LoginForm.css";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
  
    try {
      console.log(" Sende Login-Daten an Backend:", { username, password });
  
      const response = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });
  
      console.log(" API Antwort erhalten:", response.data);
  
      // Überprüfung der API-Antwort (ohne Token)
      if (!response.data || !response.data.role || !response.data.username) {
        throw new Error("Ungültige Antwort vom Server. Fehlende Daten.");
      }
  
      const { role, username: returnedUsername } = response.data;
  
      console.log(`Login erfolgreich: Benutzerrolle ${role}, Benutzername ${returnedUsername}`);
  
      // **Hier testen, ob localStorage funktioniert**
      localStorage.setItem("username", returnedUsername);
      localStorage.setItem("role", role);
  
      console.log(" localStorage gespeichert:");
      console.log("username:", localStorage.getItem("username"));
      console.log("role:", localStorage.getItem("role"));
  
      // Weiterleitung basierend auf Rolle
      if (role === "instructor") {
        navigate("/instructor");
      } else if (role === "student") {
        navigate("/student");
      } else {
        throw new Error("Unbekannte Benutzerrolle erhalten.");
      }
    } catch (err) {
      console.error(" Fehler bei der Login-Anfrage:", err);
      setError(err.response?.data?.error || "Login fehlgeschlagen. Bitte erneut versuchen.");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="actions">
            <button type="submit" className="login-button" disabled={loading}>
              {loading ? "Loading..." : "Login"}
            </button>
          </div>
        </form>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default LoginForm;
