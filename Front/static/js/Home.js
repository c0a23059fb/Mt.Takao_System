// 仮の店舗データ（後にPython連携予定）
const shops = [
  { name: "高尾山茶屋", category: "飲食" },
  { name: "山のカフェ", category: "カフェ" },
  { name: "みやげ店", category: "お土産" }
];

function searchShops() {
  const keyword = document.getElementById('searchInput').value;
  const results = shops.filter(shop =>
    shop.name.includes(keyword) || shop.category.includes(keyword)
  );
  const output = results.map(r => `<p>${r.name} (${r.category})</p>`).join('');
  document.getElementById('searchResults').innerHTML = output || "<p>該当なし</p>";
}

function connectQR() {
  // QRコード読み取りページに遷移
  window.location.href = "/qr_road";
}

function showShopSearch() {
  // 周辺店舗検索ページに遷移
  window.location.href = "/shop";
}
