import React, { createContext, useContext, useState, useEffect } from "react";

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState("ja");

  useEffect(() => {
    const saved = window.localStorage.getItem("takaoconnect-lang");
    if (saved === "ja" || saved === "en") {
      setLang(saved);
    }
  }, []);

  const toggle = () => {
    setLang((prev) => {
      const next = prev === "ja" ? "en" : "ja";
      window.localStorage.setItem("takaoconnect-lang", next);
      return next;
    });
  };

  return (
    <LanguageContext.Provider value={{ lang, toggle }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
