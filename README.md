# L News — 獨立新聞觀察（自動更新版）

香港本地 + 美股 + 世界 + 足球 新聞網站，專為 **GitHub Pages** 設計。

## ✨ 新功能（2026-07 升級）

| 功能 | 說明 |
|------|------|
| **完全自動更新** | GitHub Actions 每 **2 小時** 自動抓取最新中文新聞 |
| **美股速遞 AUTO** | 新浪財經美股快報 + RTHK 財經，中文原生 |
| **香港 / 世界 / 足球** | 香港電台 RTHK 官方 RSS（最穩定） |
| **手動編輯後台** | `editor.html` 繼續可用（適合加 X 熱議、獨家分析） |
| **X 美股熱議** | 問 Grok「更新美股 X 新聞」→ 即時翻譯 + 來源 → 貼入 editor |

## 📂 檔案結構

```
Lnewshk/
├── index.html          # 主網站
├── content.json        # 新聞資料（自動 + 手動更新）
├── editor.html         # 瀏覽器編輯後台（需 GitHub PAT）
├── update_news.py      # 自動抓新聞腳本
└── .github/workflows/
    └── update-news.yml # 定時自動更新
```

## 🚀 部署步驟（第一次）

1. **把本資料夾所有檔案覆蓋你的 repo**  
   （或直接在 GitHub 上傳 / git push）

2. **啟用 GitHub Pages**  
   - Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`

3. **啟用 Actions**（通常預設已開）  
   - 到 Actions 頁面，如果第一次會問你 enable  
   - 點 workflow 「自動更新新聞」→ Run workflow（手動測一次）

4. **完成！**  
   網站會在 `https://Lokhknews.github.io/Lnewshk/` 自動更新。

## 🔄 更新方式

### A. 全自動（推薦）
- 每 2 小時自動跑
- 你什麼都不用做
- 美股、香港、世界、足球 會一直最新

### B. 手動觸發
- 到 GitHub → Actions → 自動更新新聞 → Run workflow

### C. 加 X 上最新美股討論 / 獨家分析
1. 對我（Grok）說：  
   `更新美股X新聞` 或 `幫我抓最新TSLA / AMD / 美股討論，翻譯中文`
2. 我即刻給你完整的 JSON 文章陣列
3. 打開 `editor.html`（本地或 GitHub raw）  
   → 貼入 stock 分類 → 發布更新

### D. 改 Hero 大圖 / 今日熱話
- 繼續用 `editor.html` 最方便

## 📡 新聞來源（全部免費 + 中文優先）

- **美股**：新浪財經 `usstock.xml` + RTHK 財經
- **香港**：RTHK 本地新聞 + 政府新聞網
- **世界**：RTHK 國際 + 大中華
- **足球 / 體育**：RTHK 體育
- **趣聞**：Google News 搜尋

## 💡 進階（可選）

- 想改更新頻率：改 `.github/workflows/update-news.yml` 的 cron
- 想加更多來源：改 `update_news.py` 的 `FEEDS` 字典
- 想把 X 也全自動：需要 X API 付費方案（目前不推薦）

---

有問題直接問我！  
祝網站越來越有人氣 🚀
