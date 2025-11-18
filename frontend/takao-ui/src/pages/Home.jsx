import React from "react";
import { useNavigate } from "react-router-dom";
import ActionCard from "../components/ActionCard";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      {/* Hero */}
      <section className="hero-section">
        <div className="hero-bg" />
        <div className="hero-content">
          <p className="hero-label">Mt. TAKAO × クーポン</p>
          <h2 className="hero-title">
            登頂後のごほうびを、
            <br />
            もっとわくわくする体験に。
          </h2>
          <p className="hero-text">
            QRを読み取ってクーポンを集めたり、山頂から寄り道できるお店を探したり。
            高尾山の「その先」を楽しもう。
          </p>
        </div>
      </section>

      {/* Actions */}
      <section className="home-section">
        <h3 className="section-title">まずはここから</h3>
        <div className="action-card-grid">
          <ActionCard
            title="QRコードを読み取る"
            description="山頂やチェックポイントのQRを読み取って、クーポンやスタンプを獲得できます。"
            icon="📷"
            tag="カメラ起動"
            onClick={() => {
              // あとで Flask の /camera に接続
              window.location.href = "/camera";
            }}
          />
          <ActionCard
            title="近くのお店を探す"
            description="登頂後に立ち寄れるカフェやごはん処、お土産屋さんを地図から探せます。"
            icon="🗺"
            tag="マップ表示"
            onClick={() => navigate("/shop")}
          />
          <ActionCard
            title="持っているクーポンを見る"
            description="これまでに集めたクーポンを一覧で確認できます。有効期限もチェック。"
            icon="🎫"
            onClick={() => navigate("/coupons")}
          />
          <ActionCard
            title="チェックポイントのお題写真"
            description="撮影するお題の一覧をチェックして、高尾山のベストショットを狙おう。"
            icon="📌"
            onClick={() => navigate("/checkpoint")}
          />
        </div>
      </section>

      {/* Spots */}
      <section className="home-section">
        <h3 className="section-title">おすすめスポット</h3>
        <div className="spot-scroll">
          {["山頂の景色", "薬王院", "琵琶滝", "ケーブルカー", "高尾山口駅"].map(
            (label, i) => (
              <div className="spot-card" key={i}>
                <div className="spot-image-placeholder" />
                <p className="spot-label">{label}</p>
              </div>
            )
          )}
        </div>
      </section>
    </div>
  );
}
