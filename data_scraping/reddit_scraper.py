import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

# ---------------------------
# UTILITY FUNCTION: SAFE PRINT
# ---------------------------
def safe_print(text):
    """Print text safely to console, replacing characters that can't be printed."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode())

# ---------------------------
# ESPN ARTICLES
# ---------------------------
def scrape_espn_articles(max_articles=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    base_url = "https://www.espn.com/soccer/"
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    article_links = []
    for item in soup.select("section h1, section h2, section h3"):
        link = item.find_parent("a")["href"] if item.find_parent("a") else None
        if link:
            if not link.startswith("http"):
                link = "https://www.espn.com" + link
            article_links.append(link)

    article_links = list(set(article_links))
    safe_print(f"Found {len(article_links)} article links")

    articles_data = []
    for link in article_links[:max_articles]:
        try:
            res = requests.get(link, headers=headers)
            if res.status_code != 200:
                continue
            soup = BeautifulSoup(res.text, "html.parser")

            headline = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"
            author = soup.find("span", class_="author").get_text(strip=True) if soup.find("span", class_="author") else "N/A"
            date = soup.find("span", class_="timestamp").get_text(strip=True) if soup.find("span", class_="timestamp") else "N/A"
            paragraphs = soup.find_all("p")
            content = " ".join([p.get_text(strip=True) for p in paragraphs])

            articles_data.append({
                "headline": headline,
                "author": author,
                "date": date,
                "link": link,
                "content": content
            })
            safe_print(f" Scraped: {headline}")
            time.sleep(1)

        except Exception as e:
            safe_print(f" Failed to scrape {link}: {e}")

    return articles_data

# ---------------------------
# REDDIT POSTS + COMMENTS
# ---------------------------
def scrape_reddit(query, post_limit=5, comments_limit=3):
    url = f"https://www.reddit.com/search.json?q={query.replace(' ', '+')}&limit={post_limit}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    data = r.json()

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        post_info = {
            "title": post.get("title"),
            "author": post.get("author"),
            "subreddit": post.get("subreddit"),
            "url": "https://www.reddit.com" + post.get("permalink", ""),
            "score": post.get("score"),
            "date": datetime.datetime.fromtimestamp(post.get("created_utc", 0)).strftime("%Y-%m-%d %H:%M"),
            "content": post.get("selftext", ""),
            "comments": []
        }

        # Fetch top comments for post
        comments_url = f"https://www.reddit.com{post.get('permalink', '')}.json?limit={comments_limit}"
        comments_data = requests.get(comments_url, headers=headers).json()
        if comments_data and len(comments_data) > 1:
            for com in comments_data[1]["data"].get("children", [])[:comments_limit]:
                if com.get("kind") == "t1" and "data" in com:
                    post_info["comments"].append({
                        "author": com["data"].get("author"),
                        "body": com["data"].get("body"),
                        "score": com["data"].get("score"),
                        "date": datetime.datetime.fromtimestamp(com["data"].get("created_utc", 0)).strftime("%Y-%m-%d %H:%M")
                    })

        posts.append(post_info)
        time.sleep(1)

    return posts

# ---------------------------
# RUN SCRAPER
# ---------------------------
def run_scraper(game_query):
    safe_print(f"\n=== SCRAPING DATA FOR: {game_query} ===")

    # ESPN
    espn_articles = scrape_espn_articles(max_articles=5)

    # Reddit
    reddit_posts = scrape_reddit(game_query, post_limit=5, comments_limit=3)

    # ----- PRINT RESULTS -----
    safe_print("\n=== ESPN ARTICLES ===")
    for i, a in enumerate(espn_articles, 1):
        safe_print(f"\n[{i}] {a['headline']} (Author: {a['author']}, Date: {a['date']})")
        safe_print(f"Link: {a['link']}")
        safe_print(f"Content Preview: {a['content'][:300]}{'...' if len(a['content'])>300 else ''}")

    safe_print("\n=== REDDIT THREADS ===")
    for i, r in enumerate(reddit_posts, 1):
        safe_print(f"\n[{i}] {r['title']} (u/{r['author']}, r/{r['subreddit']}, Score: {r['score']}, Date: {r['date']})")
        safe_print(f"Link: {r['url']}")
        safe_print(f"Content Preview: {r['content'][:200]}...")
        if r['comments']:
            safe_print(" Comments:")
            for c in r['comments']:
                try:
                    safe_print(f"  - (u/{c['author']}, Score: {c['score']}, Date: {c['date']}) {c['body'][:120]}...")
                except UnicodeEncodeError:
                    safe_body = c['body'][:120].encode('ascii', errors='replace').decode()
                    safe_print(f"  - (u/{c['author']}, Score: {c['score']}, Date: {c['date']}) {safe_body}...")

    # ----- SAVE TO CSV -----
    pd.DataFrame(espn_articles).to_csv("espn_articles.csv", index=False)

    reddit_flat = []
    for r in reddit_posts:
        reddit_flat.append({
            "title": r['title'],
            "author": r['author'],
            "subreddit": r['subreddit'],
            "score": r['score'],
            "date": r['date'],
            "content": r['content'],
            "url": r['url'],
            "comments": "; ".join([f"{c['author']}({c['score']}): {c['body']}" for c in r['comments']])
        })
    pd.DataFrame(reddit_flat).to_csv("reddit_posts.csv", index=False)

    safe_print("\n✅ Data saved: espn_articles.csv, reddit_posts.csv")

# ---------------------------
# Example
# ---------------------------
if __name__ == "__main__":
    game_query = "Barcelona vs Real Madrid"
    run_scraper(game_query)
