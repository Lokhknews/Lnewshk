# L News — 轉載 X 重要貼文

香港主題站，專為 **GitHub Pages** 設計。  
內容以 **轉載 X（Twitter）上的重要貼文** 為主，附中文翻譯，**清楚標示來源，不當成原創**。

## 內容形式

每則卡片顯示：

| 欄位 | 說明 |
|------|------|
| 作者 | 顯示名 + `@handle` |
| 中文翻譯 | 前台主文（只顯示中文） |
| 時間 | 顯示用時間字串 |
| 原文連結 | 「查看原文」連到 X |
| 標示 | 固定「轉載自 X」 |

分類（五類全留）：

- **香港** / **世界** / **趣聞** / **美股** / **足球**  
- **美股** 專門放美股相關 X 貼文  

**Hero（首頁焦點）** 由你自行用 `editor.html` 維護。

## 檔案結構

```
Lnewshk/
├── index.html      # 主網站（X 貼文卡片）
├── content.json    # 資料（手動 / 半自動更新）
├── editor.html     # 瀏覽器編輯後台（需 GitHub PAT）
└── README.md
```

> 已移除 RSS 自動抓取腳本與 GitHub Actions 定時更新  
> （X 不適合免費全自動抓取；避免腳本覆寫你的轉載內容）

## 部署（第一次）

1. 把檔案 push 到 GitHub repo（例如 `Lokhknews/Lnewshk`）
2. **Settings → Pages** → Deploy from branch → `main` / `/ (root)`
3. 網站：`https://Lokhknews.github.io/Lnewshk/`

## 如何更新內容

### A. 用 editor.html（推薦）

1. 本地開啟 `editor.html`（或從 Pages 打開同一路徑）
2. 貼上 GitHub Fine-grained PAT（Contents: Read and write）
3. 「載入目前網站內容」
4. 在各分類新增轉載：貼 **X 連結**、填 **作者 / 翻譯 / 時間**
5. 按「發布更新」

貼上 `https://x.com/user/status/…` 時，若 handle 空白會自動填入。

### B. 半自動（問 Grok）

對 Grok 說例如：

> 幫我抓最新美股相關 X 討論（TSLA / NVDA），翻譯成繁中，輸出符合 Lnewshk content.json 的 JSON 陣列

把結果貼進 `editor.html` 對應分類，或直接改 `content.json` 再 commit。

### C. 直接改 content.json

單則貼文 schema：

```json
{
  "id": "x_1234567890",
  "author_name": "作者顯示名",
  "author_handle": "handle",
  "author_avatar": "",
  "x_url": "https://x.com/handle/status/1234567890",
  "posted_at": "2026-07-14T12:00:00+08:00",
  "time_display": "今天 12:00",
  "title": "可選短標題",
  "translation_zh": "中文翻譯（主文）",
  "image": "",
  "tags": ["美股"],
  "note": "",
  "attribution": "轉載自 X"
}
```

## 注意

- 本站為**轉載 + 翻譯**，請自行確認轉載／翻譯使用是否符合你的用途與平台規範。
- 不內建 X API；付費 API 全自動抓取屬進階選項，目前不建議。

有問題直接問 Grok。
