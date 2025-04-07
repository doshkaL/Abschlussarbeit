import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>Kontakt</h3>
          <p>HTW Berlin</p>
          <p>Treskowallee 8</p>
          <p>10318 Berlin</p>
          <p>Telefon: +49 30 5019-0</p>
          <p>Email: info@htw-berlin.de</p>
        </div>
        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/support">Support</a></li>
            <li><a href="/weiterbildungen">Weiterbildungen</a></li>
            <li><a href="/links">Links</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h3>Social Media</h3>
          <ul>
            <li><a href="https://facebook.com">Facebook</a></li>
            <li><a href="https://twitter.com">Twitter</a></li>
            <li><a href="https://instagram.com">Instagram</a></li>
            <li><a href="https://linkedin.com">LinkedIn</a></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} HTW Berlin. Alle Rechte vorbehalten.</p>
      </div>
    </footer>
  );
};

export default Footer;