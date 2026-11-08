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
├── .agents/
│   └── skills/
│       └── weekly-financial-report-format/
│           └── SKILL.md
├── .github/
│   └── workflows/
│       └── weekly-financial-learning.yml
├── scripts/
│   ├── auto_learn_weekly_reports.py
│   └── export_and_mail_weekly_report.py
├── AGENTS.md
├── handoff.md
├── index.html
├── .gitignore
├── 財經週報學習總綱與波克夏投資決策知識庫.md
├── 20260824-0828 | 美債殖利率飆升深度分析.gdoc
├── 20260831-0904 全球宏觀經濟與 AI 產業大變局深度解讀.md
├── 20260831-0904 | 美聯準會政策變革與「財政部放水」的強烈衝突.gdoc
├── 20260906 | 孫明德主任分析：2026 年全球債市面臨的劇烈動盪.gdoc
├── 20260907-0913 全球市場大換血與 AI 獨撐大局深度解讀.md
├── 20260907-0913 | 原油破百、美債失火！全球市場大換血，AI 如何獨撐大局？.gdoc
├── 20260921-0925 全球宏觀經濟與台灣新局深度解讀.md
├── 20260921-0925 | AI狂潮與高利率下的全球經濟與台灣新局.gdoc
├── 20260929-1002 全球宏觀經濟與 AI 豪賭深度解讀.md
├── 20260929-1002 | 美債殖利率破5%、股市卻創新高？數兆美元AI豪賭下的全球經濟剖析.gdoc
├── 20261005-1009 全球宏觀經濟與雙層世界深度解讀.md
├── 20261005-1009 | AI 狂歡與債市寒冬：走進「企業賺錢、政府缺錢、人民沒錢」的雙層世界.gdoc
├── 20261027-1030 全球宏觀經濟與 AI 科技股震盪深度解讀.md
├── 20261027-1030 科技巨頭爆雷補跌，金融市場為何迎來四年來最痛單日失血.gdoc
├── 20261102-1103 全球半導體暴跌與 AI 生產力真偽深度解讀.md
├── 20261102-1103 | 費半崩入熊市、蘋果Ａ轉！AI 生產力革命是真是假？美股跌出買點了嗎？.gdoc
├── 20261106 全球財經週報.md
├── 20261106 - 全球財經週報.gdoc
└── shorts-20261106/
    ├── index.html
    ├── 20261106_rich_financial_shorts.mp4
    ├── generate_rich_cloned_voice.py
    └── audio/
        └── voiceover.mp3
```

## 專案專用技能
- **每週財經週報文件排版** (`weekly-financial-report-format`)：**限定本專案**。觸發詞包含「排版新聞週報」、「整理財經週報」、「匯出成 google文件」、「排版財經筆記」等。嚴格遵循五大黃金規範：
  1. **四級標題階梯**：H1（24pt 主標題）/ H2（19pt 壹Why、貳How、參What）/ H3（15.5pt 一、二、三）/ H4（13.5pt （一）、（二）、（三））。
  2. **內文首行縮排**：段落強制縮排 2 字元（Google Docs 使用 `text-indent: 26pt;`，Markdown 使用 `　　`）。
  3. **最小字級規範**：全篇正文與註解皆不得小於 `12pt`（正文統一 `12.5pt`，行高 1.85）。
  4. **關鍵數字紅字粗體**：所有重要統計、碼數、百分比、金額一律以紅字粗體（`#c00000`）強調。
  5. **自動同步匯出**：自動產生 Markdown 並透過 Google Drive API Multipart 轉為標準 Google 文件，自動生成本地 `.gdoc` 捷徑。
  6. **對外合規防護（嚴禁專有商標名）**：本週報與簡報為對外公開大眾報告，**全篇絕對嚴禁出現「波克夏心法」等專有名詞**，對外一律採用通用的「頂尖價值投資視角」、「安全邊際原則」與「資本配置策略」，徹底杜絕商標侵權與法律爭議。
- **每週財經網頁簡報製作** (`weekly-financial-notes-slide`)：觸發詞包含「製作這週的財經簡報」、「製作這週的財經報告」、「更新每週財經資訊」等。使用手機優先（Mobile-First）大字版 Swiper.js 架構，將每週財經筆記轉為 7 頁白話互動簡報，支援上下順暢滾動與左右翻頁，並自動部署至 GitHub Pages。
- **每週財經短影音製作** (`shorts-video-production`)：以每週財經週報為腳本，使用本機「Rich的聲音」克隆語音模型（VoxCPM2 / Apple Silicon MPS GPU）搭配 HyperFrames 打造 9:16 直式短影音（1080x1920，30fps）。嚴格遵守：字卡字體推至畫面最大限度（標題 84px、重點數字 110-120px）、通過 WCAG AA 高對比標準、對外報告全面去除「波克夏心法」等專有名稱以防商標侵權。

## 開工 / 收工 SOP
- **開工（startup）**：讀取 `AGENTS.md` 與 `handoff.md` 確認最新進度。
- **週報排版（weekly-financial-report-format）**：依 H1-H4 階層、首行縮排、紅字數字規範排版週報，匯出 Google 文件與更新 Markdown。
- **更新簡報（weekly-financial-notes-slide）**：載入每週最新財經筆記，依規範產生 `index.html` 並發布至 Pages。
- **收工（shutdown）**：更新 `handoff.md`，進行 Git commit/push 並同步備份至 Obsidian。

