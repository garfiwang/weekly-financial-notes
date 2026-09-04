# 【筆記】每週財經資訊 - 專案藍圖

## 專案簡介
本專案專門整理與備份每週財經資訊筆記，並於每週一早上 9:00 自動同步備份至 Obsidian 的 Second Brain 知識庫。

## 層級架構與狀態
| 層級 | 平台 | 狀態 / 位置 |
|------|------|------------|
| L1 本地 | 專案資料夾 (GDrive) | `/Users/garfiwang/Library/CloudStorage/GoogleDrive-richnews168@gmail.com/我的雲端硬碟/【筆記】每週財經資訊` |
| L2 GitHub | 公開儲存庫 | `https://github.com/garfiwang/weekly-financial-notes` |
| L3 Obsidian | 第二大腦 Vault | `/Users/garfiwang/Documents/Obsidian/【筆記】每週財經資訊` |
| L4 Pages | 簡報公開網頁 | `https://garfiwang.github.io/weekly-financial-notes/` |

## 專案目標與排程
- **核心目標**：定期彙整每週財經筆記，保持版本控制與 Obsidian 雙向/單向同步。
- **自動排程**：每週一早上 09:00 (Cron Expression: `0 9 * * 1`) 自動將本專案檔案同步備份至 Obsidian 資料夾。

## 資料夾結構
```
【筆記】每週財經資訊/
├── AGENTS.md
├── handoff.md
├── index.html
├── .gitignore
├── 20260824-0828 | 美債殖利率飆升深度分析.gdoc
├── 20260831-0904 全球宏觀經濟與 AI 產業大變局深度解讀.md
└── 20260831-0904 全球宏觀經濟解讀.gdoc
```

## 專案專用技能
- **每週財經網頁簡報製作** (`weekly-financial-notes-slide`)：觸發詞包含「製作這週的財經簡報」、「製作這週的財經報告」、「更新每週財經資訊」等。使用手機優先（Mobile-First）大字版 Swiper.js 架構，將每週財經筆記轉為 7 頁白話互動簡報，支援上下順暢滾動與左右翻頁，並自動部署至 GitHub Pages。

## 開工 / 收工 SOP
- **開工（startup）**：讀取 `AGENTS.md` 與 `handoff.md` 確認最新進度。
- **更新簡報（weekly-financial-notes-slide）**：載入每週最新財經筆記，依規範產生 `index.html` 並發布至 Pages。
- **收工（shutdown）**：更新 `handoff.md`，進行 Git commit/push 並同步備份至 Obsidian。
