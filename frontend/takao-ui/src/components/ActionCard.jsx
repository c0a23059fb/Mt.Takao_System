import React from "react";

export default function ActionCard({ title, description, icon, onClick, tag }) {
  return (
    <button className="action-card" onClick={onClick}>
      <div className="action-card-icon-wrapper">
        <span className="action-card-icon">{icon}</span>
      </div>
      <div className="action-card-body">
        <div className="action-card-header">
          <h2 className="action-card-title">{title}</h2>
          {tag && <span className="action-card-tag">{tag}</span>}
        </div>
        <p className="action-card-description">{description}</p>
      </div>
    </button>
  );
}
