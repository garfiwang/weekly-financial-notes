#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每週財經週報雲端自動研讀與價值投資決策知識庫更新腳本
執行環境：GitHub Actions (雲端定時排程每週一 17:00 UTC+8)
"""

import os
import re
import sys
import glob
from datetime import datetime, timezone, timedelta

def get_taipei_now():
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz)

def scan_weekly_reports(base_dir="."):
    """掃描所有財經週報 markdown 檔案"""
    pattern = os.path.join(base_dir, "2026*.md")
    files = sorted(glob.glob(pattern))
    reports = []
    for f in files:
        fname = os.path.basename(f)
        # 排除知識庫自身
        if "知識庫" in fname or "總綱" in fname:
            continue
        # 提取日期
        match = re.match(r"(2026\d{4}-\d{4}|2026\d{4})", fname)
        date_str = match.group(1) if match else "未知日期"
        reports.append({
            "path": f,
            "filename": fname,
            "date": date_str
        })
    return reports

def parse_report_content(file_path):
    """解析單篇財經週報的核心重點"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取主標題
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(file_path)

    # 提取核心摘要
    summary_match = re.search(r"> \*\*📌【本週核心摘要】\*\*\s*(.+?)(?=\n---|\n##|$)", content, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""
    # 去除 html span tag 方便文字分析
    clean_summary = re.sub(r"<[^>]+>", "", summary).strip()

    return {
        "title": title,
        "summary": clean_summary,
        "raw_content": content
    }

def update_knowledge_base(kb_path, latest_report, all_reports):
    """檢查並更新知識庫檔案"""
    if not os.path.exists(kb_path):
        print(f"[ERROR] 找不到知識庫檔案：{kb_path}")
        return False

    with open(kb_path, "r", encoding="utf-8") as f:
        kb_text = f.read()

    latest_date = latest_report["date"]
    latest_title = latest_report["parsed"]["title"]
    latest_summary = latest_report["parsed"]["summary"]

    # 檢查該週報是否已納入知識庫
    if latest_date in kb_text and latest_title[:15] in kb_text:
        print(f"[INFO] 最新週報 {latest_date} 已完整收錄於知識庫中，無需重複添加。")
        return False

    print(f"[INFO] 偵測到最新週報尚未收錄：{latest_date} - {latest_title}")
    taipei_time_str = get_taipei_now().strftime("%Y-%m-%d %H:%M")

    # 更新最新更新時間（避免重複累積時間戳）
    if "> **最新" in kb_text:
        kb_text = re.sub(
            r"> \*\*最新.*?\n",
            f"> **最新雲端更新**：{taipei_time_str} (GitHub Actions 雲端自動同步)\n",
            kb_text,
            count=1
        )
    else:
        kb_text = re.sub(
            r"(> \*\*建立時間\*\*：.*?\n)",
            r"\1> **最新雲端更新**：" + taipei_time_str + " (GitHub Actions 雲端自動同步)\n",
            kb_text,
            count=1
        )

    # 在肆、當前節點前追加節點備註
    update_note = f"\n\n### 📌 最新週期動態追加（{latest_date}）：{latest_title}\n"
    update_note += f"- **核心宏觀摘要**：{latest_summary}\n"
    update_note += f"- **頂尖價值投資視角檢驗**：在 {latest_date} 的市場震盪中，持續檢視實質盈餘（Owner Earnings）與安全邊際（Margin of Safety），嚴格落實非對稱賠率配置。\n"

    # 在肆、當前節點前插入
    insert_pos = kb_text.find("## 肆、")
    if insert_pos != -1:
        new_kb_text = kb_text[:insert_pos] + update_note + "\n---\n\n" + kb_text[insert_pos:]
    else:
        new_kb_text = kb_text + update_note

    with open(kb_path, "w", encoding="utf-8") as f:
        f.write(new_kb_text)

    print(f"[SUCCESS] 知識庫 {kb_path} 已成功增補最新週報分析！")
    return True

def update_handoff_log(handoff_path, latest_report):
    """更新 handoff.md 紀錄"""
    if not os.path.exists(handoff_path):
        return

    with open(handoff_path, "r", encoding="utf-8") as f:
        handoff_text = f.read()

    taipei_now = get_taipei_now().strftime("%Y-%m-%d %H:%M")
    latest_date = latest_report["date"]

    log_entry = f"- [x] **[雲端不斷電 GitHub Actions] 自動研讀與同步** ({taipei_now})：完成最新週報 `{latest_date}` 檢查與價值投資決策知識庫自動增補。\n"

    # 在 ## ⏯️ 目前做到哪 底下追加
    if "## ⏯️ 目前做到哪" in handoff_text:
        handoff_text = handoff_text.replace(
            "## ⏯️ 目前做到哪\n",
            f"## ⏯️ 目前做到哪\n{log_entry}"
        )

    # 更新最後更新時間
    handoff_text = re.sub(
        r"- \*\*時間\*\*：.*",
        f"- **時間**：{taipei_now}",
        handoff_text
    )
    handoff_text = re.sub(
        r"- \*\*更新者\*\*：.*",
        f"- **更新者**：GitHub Actions (雲端不斷電自動研讀任務)",
        handoff_text
    )

    with open(handoff_path, "w", encoding="utf-8") as f:
        f.write(handoff_text)

    print(f"[SUCCESS] handoff.md 已成功更新日誌。")

def main():
    print("=" * 60)
    print(f"啟動每週財經週報雲端自動研讀程序 ({get_taipei_now().strftime('%Y-%m-%d %H:%M:%S')} 台北時間)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    reports = scan_weekly_reports(base_dir)
    print(f"[INFO] 掃描到 {len(reports)} 份財經週報檔案。")

    if not reports:
        print("[WARNING] 未發現任何財經週報檔案，結束程序。")
        sys.exit(0)

    for r in reports:
        r["parsed"] = parse_report_content(r["path"])

    latest_report = reports[-1]
    print(f"[INFO] 最新週報為：{latest_report['date']} | {latest_report['parsed']['title']}")

    kb_path = os.path.join(base_dir, "財經週報學習總綱與波克夏投資決策知識庫.md")
    handoff_path = os.path.join(base_dir, "handoff.md")

    updated = update_knowledge_base(kb_path, latest_report, reports)

    if updated:
        update_handoff_log(handoff_path, latest_report)
        print("[COMPLETE] 檔案更新完成，準備由 Git 自動提交變更。")
    else:
        print("[COMPLETE] 知識庫內容已為最新狀態，無需提交變更。")

if __name__ == "__main__":
    main()
