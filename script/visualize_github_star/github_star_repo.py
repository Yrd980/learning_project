import requests
import json
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm  # 需要安装：pip install tqdm

# 配置参数
TOKEN = ""  # 替换为你的 GitHub Token
HEADERS = {"Authorization": f"token {TOKEN}"}
PER_PAGE = 100      # 每页数量 (GitHub 最大允许 100)
TIMEOUT = 10        # 请求超时时间（秒）
MAX_RETRIES = 3     # 最大重试次数

def setup_session():
    """配置带重试机制的 Session"""
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_all_starred(session):
    """获取所有星标仓库数据"""
    page = 1
    repos = []
    with tqdm(desc="📥 Fetching pages", unit="page", leave=False) as pbar:
        while True:
            url = f"https://api.github.com/users/username/starred?per_page={PER_PAGE}&page={page}"
            try:
                response = session.get(url, headers=HEADERS, timeout=TIMEOUT)
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break
                
                repos.extend(data)
                pbar.set_postfix({"repos": len(repos)})
                pbar.update(1)
                page += 1

            except Exception as e:
                print(f"\n⚠️ Error on page {page}: {str(e)}")
                break
    return repos

def save_data(repos):
    """保存数据到 JSON 和 CSV"""
    # 保存为 JSON
    with open("starred_repos.json", "w") as f:
        json.dump(repos, f, indent=2)

    # 保存为 CSV
    with open("starred_repos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name", "URL", "Description", 
            "Language", "Stars", "Archived"
        ])
        
        for repo in tqdm(repos, desc="💾 Saving CSV", unit="repo"):
            writer.writerow([
                repo["full_name"],
                repo["html_url"],
                repo["description"] or "",  # 处理 null 值
                repo["language"] or "N/A",
                repo["stargazers_count"],
                repo["archived"]
            ])

if __name__ == "__main__":
    print("🚀 Starting GitHub Starred Repos Export")
    
    # 初始化 Session
    session = setup_session()
    
    # 获取所有仓库数据
    print("⏳ Downloading repository data...")
    repositories = fetch_all_starred(session)
    
    # 保存数据
    print(f"\n✅ Downloaded {len(repositories)} repositories")
    save_data(repositories)
    
    # 结果输出
    print("\n🎉 Export completed!")
    print(f"📂 JSON file: starred_repos.json")
    print(f"📊 CSV file: starred_repos.csv")
