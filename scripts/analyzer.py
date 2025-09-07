import feedparser
import os
import openai
import markdown
import yaml
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from pathlib import Path

class DemocracyNormsMonitor:
    def __init__(self, openai_api_key, norms_path="_norms", output_path="_events"):
        openai.api_key = openai_api_key
        self.norms_path = norms_path
        self.output_path = output_path
        self.norms = self.load_norms()

    def load_norms(self):
        norms = {}
        for file in Path(self.norms_path).glob("*.md"):
            with open(file, 'r') as f:
                content = f.read()
                parts = content.split('---')
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1])
                    body = parts[2]
                    norms[front_matter.get('title')] = body.strip()
        return norms

    def fetch_rss_articles(self, feed_url, max_entries=5):
        feed = feedparser.parse(feed_url)
        return feed.entries[:max_entries]

    def fetch_url_text(self, url):
        try:
            with urlopen(url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                paragraphs = soup.find_all('p')
                return '\n'.join(p.get_text() for p in paragraphs)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def analyze_against_norms(self, text):
        prompt = f"""
You are a political analyst assistant trained in identifying violations or upholding of democratic norms.
Given the article text below, determine whether it appears to violate or uphold any of the following democratic norms, defined below. Return only those that are clearly violated or upheld.

Democratic Norms:
{chr(10).join([f"- {title}: {desc[:160]}..." for title, desc in self.norms.items()])}

Article Text:
{text[:3000]}

Return a summary of the event, the most relevant violated or upheld norms (by title), and why.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message['content']

    def generate_markdown_entry(self, title, actor, summary, norms, link):
        slug = title.lower().replace(" ", "-").replace("'", "")
        filename = f"{self.output_path}/{slug}.md"
        front_matter = {
            'title': title,
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'actor': actor,
            'description': summary.split('\n')[0][:140],
            'link': link
        }
        md_content = f"---\n{yaml.dump(front_matter)}---\n\n{summary.strip()}\n\n**Tagged Norms:** {', '.join(norms)}"
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            f.write(md_content)
        print(f"Saved: {filename}")

    def process_rss_feed(self, feed_url):
        articles = self.fetch_rss_articles(feed_url)
        for entry in articles:
            text = self.fetch_url_text(entry.link)
            if text:
                analysis = self.analyze_against_norms(text)
                # You could use regex or OpenAI again to extract norms & actor from analysis
                actor = "Unknown"
                norms = [k for k in self.norms if k.lower() in analysis.lower()]
                self.generate_markdown_entry(entry.title, actor, analysis, norms, entry.link)
                
if __name__ == "__main__":
    monitor = DemocracyNormsMonitor(openai_api_key=os.getenv("OPENAI_API_KEY"))
    monitor.process_rss_feed("https://www.npr.org/rss/rss.php?id=1001")  # NPR Politics RSS feed