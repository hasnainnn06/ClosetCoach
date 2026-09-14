import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "../src/components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "../pages/Home";
import About from "../pages/About";
import OutfitGenerator from "../pages/OutfitGenerator";
import CIR from "../pages/CIR";
import Demo from "../pages/Demo";
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import Wardrobe from "../pages/Wardrobe";
import SavedLooks from "../pages/SavedLooks";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/outfit-generator" element={
            <ProtectedRoute>
              <OutfitGenerator />
            </ProtectedRoute>
          } />
          <Route path="/cir" element={
            <ProtectedRoute>
              <CIR />
            </ProtectedRoute>
          } />
          <Route path="/wardrobe" element={
            <ProtectedRoute>
              <Wardrobe />
            </ProtectedRoute>
          } />
          <Route path="/saved-looks" element={
            <ProtectedRoute>
              <SavedLooks />
            </ProtectedRoute>
          } />
          <Route path="/demo" element={<Demo />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* safety net */}
          <Route path="*" element={<h2 style={{ padding: 20 }}>Page Not Found</h2>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;

