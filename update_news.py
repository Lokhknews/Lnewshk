#!/usr/bin/env python3
"""
L News 自動更新腳本
從免費中文 RSS 抓取最新新聞，更新 content.json 的 categories
保留 hero 不變（用 editor.html 手動更新）
適合 GitHub Actions 每小時 / 每天跑
"""

import json
import feedparser
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import html
import hashlib

# ========== 設定 ==========
CONTENT_FILE = Path("content.json")
MAX_PER_CAT = 8          # 每個分類最多保留幾篇
TZ = timezone(timedelta(hours=8))  # 香港時間

# 免費中文 RSS 來源（2026 仍穩定）
FEEDS = {
    "hk": [
        "https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml",
        "https://www.news.gov.hk/tc/common/html/topstories.rss.xml",
    ],
    "world": [
        "https://rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml",
        "https://rthk.hk/rthk/news/rss/c_expressnews_egreaterchina.xml",
    ],
    "stock": [
        "http://rss.sina.com.cn/finance/usstock.xml",          # 新浪美股快報（中文）
        "https://rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml",  # RTHK 財經
        "https://finance.yahoo.com/news/rssindex",            # Yahoo 英文 backup
    ],
    "football": [
        "https://rthk.hk/rthk/news/rss/c_expressnews_csport.xml",
    ],
    "fun": [
        # 可以用 Google News 或之後加
        "https://news.google.com/rss/search?q=%E8%B6%A3%E8%81%9E+OR+%E5%A8%9B%E6%A8%82&hl=zh-TW&gl=HK&ceid=HK:zh-Hant",
    ],
}

CAT_LABEL = {
    "hk": "香港新聞",
    "world": "世界新聞",
    "fun": "趣聞",
    "stock": "美股速遞",
    "football": "足球",
}


def clean_text(text: str, max_len: int = 220) -> str:
    if not text:
        return ""
    # 去掉 HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0] + "…"
    return text


def parse_time(entry) -> str:
    """轉成香港時間顯示字串"""
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).astimezone(TZ)
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            dt = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).astimezone(TZ)
        else:
            dt = datetime.now(TZ)
        # 如果是今天就顯示「今天 HH:MM」
        now = datetime.now(TZ)
        if dt.date() == now.date():
            return f"今天 {dt.strftime('%H:%M')}"
        elif (now.date() - dt.date()).days == 1:
            return f"昨天 {dt.strftime('%H:%M')}"
        else:
            return dt.strftime("%m-%d %H:%M")
    except Exception:
        return datetime.now(TZ).strftime("今天 %H:%M")


def fetch_category(cat: str) -> list:
    """抓取一個分類的最新文章"""
    articles = []
    seen_titles = set()

    for feed_url in FEEDS.get(cat, []):
        try:
            print(f"  Fetching {feed_url} ...")
            feed = feedparser.parse(feed_url)
            if feed.bozo and not feed.entries:
                print(f"    Warning: feed error {feed.bozo_exception}")
                continue

            for entry in feed.entries[:12]:  # 多抓一點再過濾
                title = clean_text(entry.get("title", ""), 100)
                if not title or title in seen_titles:
                    continue
                # 過濾太短或無關
                if len(title) < 8:
                    continue

                summary = clean_text(
                    entry.get("summary", "") or entry.get("description", ""), 260
                )
                link = entry.get("link", "")
                source = feed.feed.get("title", "新聞來源")[:30]
                # 美化來源名稱
                if "rthk" in feed_url.lower() or "香港電台" in source:
                    source = "香港電台 RTHK"
                elif "sina" in feed_url.lower():
                    source = "新浪財經"
                elif "yahoo" in feed_url.lower():
                    source = "Yahoo Finance"
                elif "news.gov.hk" in feed_url:
                    source = "香港政府新聞網"
                elif "google" in feed_url:
                    source = "Google 新聞"

                # 簡單判斷是否像分析文
                analysis = any(k in title + summary for k in ["分析", "評論", "觀察", "觀點", "署名"])

                articles.append({
                    "title": title,
                    "time": parse_time(entry),
                    "summary": summary or title,
                    "source": source,
                    "analysis": analysis,
                    "image": "",
                    "link": link,
                })
                seen_titles.add(title)

                if len(articles) >= MAX_PER_CAT:
                    break
        except Exception as e:
            print(f"    Error fetching {feed_url}: {e}")
            continue

        if len(articles) >= MAX_PER_CAT:
            break

    # 按時間粗略排序（今天 > 昨天）
    def sort_key(a):
        t = a["time"]
        if t.startswith("今天"):
            return (0, t)
        if t.startswith("昨天"):
            return (1, t)
        return (2, t)

    articles.sort(key=sort_key)
    return articles[:MAX_PER_CAT]


def main():
    print("=" * 50)
    print("L News 自動更新開始", datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    # 讀取現有 content（保留 hero）
    if CONTENT_FILE.exists():
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        content = {"hero": {}, "categories": {}}

    # 更新每個分類
    new_categories = {}
    for cat in ["hk", "world", "fun", "stock", "football"]:
        print(f"\n[{CAT_LABEL[cat]}]")
        arts = fetch_category(cat)
        new_categories[cat] = arts
        print(f"  → 成功取得 {len(arts)} 篇")

    content["categories"] = new_categories

    # 寫回
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print("✅ content.json 已更新！")
    print(f"   香港: {len(new_categories['hk'])} | 世界: {len(new_categories['world'])} | 趣聞: {len(new_categories['fun'])}")
    print(f"   美股: {len(new_categories['stock'])} | 足球: {len(new_categories['football'])}")
    print("=" * 50)


if __name__ == "__main__":
    main()
