#!/usr/bin/env python3
"""
Drana-Infinity Auto Updater
---------------------------
Designed and maintained by IHA089.
"""

import os
from git import Repo, GitCommandError

def update_drana_infinity(repo_dir: str = "."):
    print("\n|──(Checking for Drana-Infinity Updates)──|")

    # Perlu diperiksa karena Anda menjalankan ini di folder yang baru di-git init
    if not os.path.exists(os.path.join(repo_dir, ".git")):
        print("This directory is not a Git repository. Skipping update check.")
        return False

    try:
        repo = Repo(repo_dir)
        origin = repo.remotes.origin
        # Fetching dari branch 'main' untuk membandingkan
        origin.fetch(refspec='main:main') 

        local_commit = repo.head.commit.hexsha
        
        # Menggunakan origin.refs.main untuk memastikan kita merujuk ke branch 'main'
        if 'main' not in origin.refs:
            print("Error: Remote branch 'main' not found. Check your remote setup.")
            return False

        remote_commit = origin.refs.main.commit.hexsha

        if local_commit != remote_commit:
            print(f"Update found!")
            try:
                # Menggunakan --include-untracked bersama stash
                repo.git.stash('push', '-u', '-m', 'Auto-stash before update')
            except GitCommandError as e:
                # Aman untuk diabaikan jika tidak ada perubahan untuk distash
                if "No local changes to save" not in str(e):
                    pass

            print("Pulling latest version from GitHub...")
            # Secara eksplisit pull branch 'main'
            origin.pull('main')

            try:
                # Mencoba memulihkan stash terakhir
                repo.git.stash('pop')
            except GitCommandError:
                # Aman untuk diabaikan jika tidak ada stash untuk dipulihkan
                pass  

            print("Drana-Infinity successfully updated!")
            return True
        else:
            print(" Already up to date. No updates available.")
            return False

    except GitCommandError as e:
        # Menangkap error Git spesifik
        print(f"Git error: {e}")
        return False
    except Exception as e:
        # Menangkap error umum lainnya
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    update_drana_infinity()