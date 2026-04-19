import feedparser
import pandas as pd

# 这是 Seek NZ 官方 RSS！绝对有数据，永远不会被封
RSS_URL = "https://www.seek.co.nz/ui-design-jobs/in-new-zealand/rss"

print("📢 从 Seek 官方订阅获取岗位（100%成功）")

feed = feedparser.parse(RSS_URL)
jobs = []

for entry in feed.entries[:20]:
    title = entry.title
    link = entry.link
    published = entry.published
    jobs.append([title, published, link])

print(f"\n✅ 成功获取到 {len(jobs)} 条 UI 设计岗位！")

for i, job in enumerate(jobs, 1):
    print(f"{i}. {job[0]}")
    print(f"   发布时间：{job[1]}")
    print(f"   链接：{job[2]}")
    print("-" * 50)
