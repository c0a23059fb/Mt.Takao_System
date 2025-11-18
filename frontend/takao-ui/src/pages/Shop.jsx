import React, { useState } from "react";

const ALL = "all";

const shopsMock = [
  {
    id: 1,
    name: "高尾山口カフェ",
    category: "cafe",
    time: "10:00〜18:00",
    distance: "高尾山口駅から徒歩2分",
    comment: "登山前後に一息つけるカフェ。軽食とスイーツが充実。",
  },
  {
    id: 2,
    name: "山頂ソフトクリーム屋",
    category: "sweets",
    time: "9:30〜16:00",
    distance: "山頂広場すぐそば",
    comment: "ごほうびにぴったりなソフトクリームが人気。",
  },
  {
    id: 3,
    name: "ふもとのお土産屋さん",
    category: "souvenir",
    time: "9:00〜19:00",
    distance: "ケーブルカー清滝駅前",
    comment: "高尾山限定のお菓子やキーホルダーがそろっています。",
  },
  {
    id: 4,
    name: "高尾クラフトビールバー",
    category: "restaurant",
    time: "11:00〜22:00",
    distance: "高尾山口駅から徒歩5分",
    comment: "地元のクラフトビールとおつまみが楽しめるお店。",
  },
];

const FILTERS = [
  { key: ALL, label: "すべて" },
  { key: "cafe", label: "カフェ" },
  { key: "restaurant", label: "ごはん" },
  { key: "sweets", label: "スイーツ" },
  { key: "souvenir", label: "お土産" },
];

export default function Shop() {
  const [filter, setFilter] = useState(ALL);

  const filtered = shopsMock.filter(
    (s) => filter === ALL || s.category === filter
  );

  return (
    <div className="shops-page">
      <h2 className="page-title">周辺のお店を探す</h2>
      <p className="page-description">
        高尾山の登山前後に立ち寄れるお店の例です。カテゴリで絞り込んでイメージをふくらませておけます。
      </p>

      <div className="shop-filters">
        {FILTERS.map((f) => (
          <button
            key={f.key}
            className={
              "chip-button" + (filter === f.key ? " chip-button-active" : "")
            }
            onClick={() => setFilter(f.key)}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="shop-list">
        {filtered.map((shop) => (
          <article key={shop.id} className="shop-card">
            <header className="shop-header">
              <h3 className="shop-name">{shop.name}</h3>
              <span className="shop-category">
                {
                  FILTERS.find((f) => f.key === shop.category)?.label ??
                  "その他"
                }
              </span>
            </header>
            <p className="shop-distance">{shop.distance}</p>
            <p className="shop-time">営業時間：{shop.time}</p>
            <p className="shop-comment">{shop.comment}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
