import re
import requests
from bs4 import BeautifulSoup
from mlc_chat import ChatModule


def scrape(url: str, length: int = 1024) -> str:
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")
    content = " ".join(soup.text[:length].split())
    return content


def harvest_url(prompt: str) -> str:
    # urls = re.search("(?P<url>https?://[^\s]+)", prompt).group("url")
    urls = re.findall(r"(https?://\S+)", prompt)
    print(urls)
    return urls[0]


def digest(chat_mod: ChatModule, prompt: str) -> str:
    url = harvest_url(prompt)
    content = scrape(url)
    content = content[:1024]
    summary = chat_mod.generate(
        prompt=f"Please summarize the content of this text: {content}"
    )
    return summary
