import React from "react";
import { useLanguage } from "../LanguageContext";

export default function AppHeader() {
  const { lang, toggle } = useLanguage();

  const title = "高尾コネクト";
  const subtitleJa = "登頂後の「次の一歩」を、もっと楽しく。";
  const subtitleEn = "Make your next step after the summit more enjoyable.";

  return (
    <header className="app-header">
      <div className="app-header-inner">
        <div className="app-logo-circle">⛰</div>
        <div className="app-title-group">
          <h1 className="app-title">{title}</h1>
          <p className="app-subtitle">
            {lang === "ja" ? subtitleJa : subtitleEn}
          </p>
        </div>
        <button className="lang-toggle" onClick={toggle}>
          {lang === "ja" ? "EN" : "日"}
        </button>
      </div>
    </header>
  );
}