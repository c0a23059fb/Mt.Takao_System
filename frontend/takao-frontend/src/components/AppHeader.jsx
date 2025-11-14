import React from "react";

export default function AppHeader() {
  return (
    <header className="app-header">
      <div className="app-header-inner">
        <div className="app-logo-circle">⛰</div>
        <div className="app-title-group">
          <h1 className="app-title">高尾コネクト</h1>
          <p className="app-subtitle">
            登頂後の「次の一歩」を、もっと楽しく。
          </p>
        </div>
      </div>
    </header>
  );
}
