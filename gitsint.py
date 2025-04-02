import requests
import re
import os
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import time

def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return [repo['name'] for repo in response.json() if not repo['fork']]
    return []

def get_repo_commits(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return [commit['sha'] for commit in response.json() if commit['author'] and commit['author']['login'] == username]
    return []

def process_commit(username, repo, commit_sha):
    patch_url = f"https://github.com/{username}/{repo}/commit/{commit_sha}.patch"
    response = requests.get(patch_url)
    
    if response.status_code == 200:
        content = response.text
        email_pattern = r'From:.*?<([^>]+)>'
        matches = re.findall(email_pattern, content)
        valid_emails = [email for email in matches if 'users.noreply.github.com' not in email]
        return valid_emails, patch_url
    return [], None

def save_email(email, commit_url):
    with open('results.txt', 'a') as f:
        f.write(f"Email: {email}\nFound in: {commit_url}\n\n")
    print(f"Found email: {email}")
    print(f"Commit URL: {commit_url}\n")

def main():
    github_url = input("Enter GitHub user URL (e.g., https://github.com/maxmoodycyber): ")
    username = github_url.split('/')[-1].strip()
    
    print(f"Scanning repositories for user: {username}")
    print("Note: Only scanning non-fork repositories and commits made by the user")
    
    with open('results.txt', 'w') as f:
        f.write(f"Email scan results for GitHub user: {username}\n")
        f.write("=" * 50 + "\n\n")
    
    repos = get_user_repos(username)
    if not repos:
        print("No non-fork repositories found or error accessing GitHub API")
        return
    
    print(f"Found {len(repos)} non-fork repositories to scan")
    
    unique_emails = set()
    
    for repo in repos:
        print(f"\nProcessing repository: {repo}")
        commits = get_repo_commits(username, repo)
        
        if not commits:
            print(f"No commits found for {repo} made by {username}")
            continue
            
        print(f"Found {len(commits)} commits to scan")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for commit_sha in commits:
                futures.append(executor.submit(process_commit, username, repo, commit_sha))
            
            for future in futures:
                emails, commit_url = future.result()
                for email in emails:
                    if email not in unique_emails:
                        unique_emails.add(email)
                        save_email(email, commit_url)
        
        time.sleep(1)
    
    print(f"\nScan complete! Found {len(unique_emails)} unique email addresses")
    print("All results saved to results.txt")

if __name__ == "__main__":
    main() 