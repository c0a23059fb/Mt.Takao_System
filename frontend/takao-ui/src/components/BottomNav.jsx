import React from "react";
import { NavLink } from "react-router-dom";
import { useLanguage } from "../LanguageContext";

function NavItem({ to, label, icon }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        "bottom-nav-item" + (isActive ? " bottom-nav-item-active" : "")
      }
    >
      <span className="bottom-nav-icon">{icon}</span>
      <span className="bottom-nav-label">{label}</span>
    </NavLink>
  );
}

export default function BottomNav() {
  const { lang } = useLanguage();

  return (
    <nav className="bottom-nav">
      <NavItem
        to="/"
        label={lang === "ja" ? "ホーム" : "Home"}
        icon="🏠"
      />
      <NavItem
        to="/coupons"
        label={lang === "ja" ? "クーポン" : "Coupons"}
        icon="🎫"
      />
      <NavItem
        to="/shop"
        label={lang === "ja" ? "周辺" : "Nearby"}
        icon="🗺"
      />
      <NavItem
        to="/checkpoint"
        label={lang === "ja" ? "チェック" : "Check"}
        icon="📷"
      />
    </nav>
  );
}