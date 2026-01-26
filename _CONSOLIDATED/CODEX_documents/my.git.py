import os
import time
from git import Repo

# --- CONFIGURATION ---
ROOT_DIR = "/home/sauron/unexusi/"

def get_git_status(repo_path):
    """Returns a status dictionary for a single repo."""
    try:
        repo = Repo(repo_path)
        status = {"path": repo_path, "name": os.path.basename(repo_path), "dirty": False, "ahead": 0, "behind": 0, "repo": repo}
        
        # 1. Check Local
        if repo.is_dirty(untracked_files=True):
            status["dirty"] = True

        # 2. Check Sync (Fetch hiddenly)
        try:
            origin = repo.remotes.origin
            origin.fetch()
            local_branch = repo.active_branch
            remote_branch = local_branch.tracking_branch()
            
            if remote_branch:
                status["behind"] = sum(1 for c in repo.iter_commits(f'{local_branch.name}..{remote_branch.name}'))
                status["ahead"] = sum(1 for c in repo.iter_commits(f'{remote_branch.name}..{local_branch.name}'))
        except:
            pass 
        return status
    except:
        return None

def sync_repo(repo_data, auto_message="Auto-sync via Fleet Commander"):
    """Helper to sync a single repo"""
    print(f"   ⚙️  Processing: {repo_data['name']}...")
    repo = repo_data['repo']
    
    # Save
    if repo_data['dirty']:
        repo.git.add(all=True)
        repo.index.commit(auto_message)
        print("      ✅ Local changes saved.")
    
    # Push/Pull
    try:
        origin = repo.remotes.origin
        if repo_data['behind'] > 0:
            origin.pull()
            print("      ✅ Pulled down new changes.")
        if repo_data['dirty'] or repo_data['ahead'] > 0: # If we just saved, we are now ahead
            origin.push()
            print("      ✅ Pushed up to Cloud.")
            
        if not repo_data['dirty'] and repo_data['ahead'] == 0 and repo_data['behind'] == 0:
            print("      ✨ Already clean.")
            
    except Exception as e:
        print(f"      ❌ Error syncing: {e}")

def main_dashboard():
    while True: # <--- THE LOOP (Keeps running)
        os.system('clear') # Clears screen for a fresh look (Use 'cls' if on Windows)
        print(f"\n🌍 --- UNEXUSI FLEET COMMANDER (v5.0) ---")
        print(f"Scanning Fleet in: {ROOT_DIR}...\n")

        repos_found = []
        
        # SCAN
        for folder_name in os.listdir(ROOT_DIR):
            folder_path = os.path.join(ROOT_DIR, folder_name)
            if os.path.isdir(folder_path) and os.path.isdir(os.path.join(folder_path, ".git")):
                stat = get_git_status(folder_path)
                if stat:
                    repos_found.append(stat)
                    
                    # Status Logic for Display
                    icon = "✅"
                    msg = "Synced"
                    if stat["dirty"]:
                        icon = "⚠️ "
                        msg = "Unsaved Work"
                    elif stat["ahead"] > 0:
                        icon = "⬆️ "
                        msg = f"Ahead (+{stat['ahead']})"
                    elif stat["behind"] > 0:
                        icon = "⬇️ "
                        msg = f"Behind (-{stat['behind']})"
                    
                    print(f" {len(repos_found)}. {icon} {stat['name']:<25} | {msg}")

        if not repos_found:
            print("No repositories found.")
            break

        print("\n-------------------------------------------")
        print(" A. Sync ALL repositories (Batch Mode)")
        print(" R. Refresh List")
        print(" Q. Quit")
        
        choice = input("\nCommand >> ").lower()
        
        if choice == 'q':
            print("Exiting. Have a great session!")
            break
        elif choice == 'r':
            continue # Just loops back to scan again
        elif choice == 'a':
            print("\n🚀 STARTING BATCH SYNC...")
            for repo_data in repos_found:
                sync_repo(repo_data)
            input("\nBatch complete! Press Enter to return to menu...")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(repos_found):
                target = repos_found[idx]
                print(f"\n🚀 Managing: {target['name']}")
                
                # Manual interaction
                if input("   Sync this repo? (y/n): ").lower() == 'y':
                    sync_repo(target, auto_message=input("   Enter commit message: "))
                
                input("\nDone. Press Enter...")

if __name__ == "__main__":
    main_dashboard()
