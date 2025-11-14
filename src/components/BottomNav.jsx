import React from "react";
import { NavLink } from "react-router-dom";

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
  return (
    <nav className="bottom-nav">
      <NavItem to="/" label="ホーム" icon="🏠" />
      <NavItem to="/coupons" label="クーポン" icon="🎫" />
      <NavItem to="/shop" label="周辺" icon="🗺" />
      <NavItem to="/checkpoint" label="チェック" icon="📷" />
    </nav>
  );
}
