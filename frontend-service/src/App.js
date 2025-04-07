import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginForm from "./components/Login/LoginForm";
import Navbar from "./navbar/Navbar";
import InstructorDashboard from "./pages/InstructorDashboard";
import StudentDashboard from "./pages/StudentDashboard";
import Footer from "./components/Footer/Footer";
import "./input.css";

const App = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow"> 
          <Routes>
            <Route path="/" element={<LoginForm />} />
            <Route path="/instructor" element={<InstructorDashboard />} />
            <Route path="/student" element={<StudentDashboard />} />
            <Route path="/login" element={<LoginForm />} />
          </Routes>
        </main>
        <Footer /> 
      </div>
    </Router>
  );
};

export default App;