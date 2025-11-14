import React from "react";
import { Routes, Route } from "react-router-dom";
import AppHeader from "./components/AppHeader";
import BottomNav from "./components/BottomNav";
import Home from "./pages/Home";
import Coupons from "./pages/Coupons";
import Shop from "./pages/Shop";
import Checkpoint from "./pages/Checkpoint";

export default function App() {
  return (
    <div className="app-root">
      <AppHeader />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/coupons" element={<Coupons />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/checkpoint" element={<Checkpoint />} />
        </Routes>
      </main>
      <BottomNav />
    </div>
  );
}
