import React from "react";

const missions = [
  {
    id: 1,
    title: "山頂の標識と一緒に撮影",
    spot: "山頂",
    hint: "山頂広場の『599m』の標識を背景に入れてみよう。",
  },
  {
    id: 2,
    title: "薬王院の門を背景に撮影",
    spot: "薬王院",
    hint: "仁王門の前で全体が入るように撮るのがおすすめ。",
  },
  {
    id: 3,
    title: "ケーブルカーと線路の写真",
    spot: "ケーブルカー清滝駅",
    hint: "出発前後のタイミングで、安全な場所から撮影しよう。",
  },
  {
    id: 4,
    title: "琵琶滝の水しぶきショット",
    spot: "琵琶滝",
    hint: "他の参拝者の迷惑にならない位置から静かに撮ろう。",
  },
];

export default function Checkpoint() {
  return (
    <div className="checkpoint-page">
      <h2 className="page-title">チェックポイントのお題一覧</h2>
      <p className="page-description">
        高尾山の各スポットで撮影するお題の例です。実証実験では、ここに表示されたお題を参考に写真を撮影し、確認後にクーポンが発行されます。
      </p>

      <div className="checkpoint-list">
        {missions.map((m) => (
          <article key={m.id} className="checkpoint-card">
            <header className="checkpoint-header">
              <h3 className="checkpoint-title">{m.title}</h3>
              <span className="checkpoint-spot">@{m.spot}</span>
            </header>
            <p className="checkpoint-hint">{m.hint}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
