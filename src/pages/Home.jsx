import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Link } from "react-router-dom"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-green-100 pb-24">
      {/* ---------- ヘッダー ---------- */}
      <header className="backdrop-blur bg-white/70 border-b sticky top-0 z-10">
        <div className="max-w-3xl mx-auto flex items-center justify-between px-4 py-3">
          <h1 className="text-lg font-semibold text-gray-700">
            高尾コネクト
          </h1>
          <div className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full">
            登頂後のごほうび
          </div>
        </div>
      </header>

      {/* ---------- Hero Section ---------- */}
      <div className="max-w-3xl mx-auto px-4 mt-6">
        <div className="rounded-3xl p-6 bg-gradient-to-r from-green-200 to-green-300 shadow-md">
          <h2 className="text-xl font-semibold text-gray-700 leading-relaxed">
            登頂後のごほうびを、
            <br />
            もっとわくわくする体験に。
          </h2>
          <p className="text-sm text-gray-600 mt-2">
            QRを読み取ってクーポンを集めたり、山頂から寄り道できるお店を探したり。
          </p>
        </div>
      </div>

      {/* ---------- アクションカード ---------- */}
      <div className="max-w-3xl mx-auto px-4 mt-6 grid grid-cols-2 gap-4">
        <ActionLink to="/qr" icon="📷" label="QRコードを読み取る" badge="カメラ起動" />
        <ActionLink to="/nearby" icon="🗺️" label="近くのお店を探す" badge="マップ表示" />
        <ActionLink to="/coupons" icon="🎫" label="持っているクーポンを見る" />
        <ActionLink to="/checkpoint" icon="📸" label="チェックポイントの写真" />
      </div>

      {/* ---------- スポット横スクロール ---------- */}
      <div className="max-w-3xl mx-auto px-4 mt-10">
        <h3 className="text-gray-700 font-semibold mb-3">おすすめスポット</h3>

        <div className="flex gap-4 overflow-x-auto pb-2 hide-scrollbar">
          {["山頂の景色", "薬王院", "琵琶滝", "ケーブルカー", "高尾山口駅"].map((spot) => (
            <Card
              key={spot}
              className="min-w-[160px] h-28 bg-gradient-to-br from-green-200 to-green-300 rounded-2xl shadow-sm"
            >
              <CardContent className="flex items-end p-4 text-gray-700 font-medium">
                {spot}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}

/* ---------- 小さいアクションカードの共通コンポーネント ---------- */
function ActionLink({ to, icon, label, badge }) {
  return (
    <Link to={to}>
      <Card className="rounded-2xl shadow-sm hover:shadow-md transition-all">
        <CardContent className="p-4 flex flex-col gap-2">
          <div className="text-3xl">{icon}</div>
          <div className="text-gray-700 font-medium">{label}</div>
          {badge && (
            <Badge variant="secondary" className="text-xs self-start mt-1">
              {badge}
            </Badge>
          )}
        </CardContent>
      </Card>
    </Link>
  )
}
