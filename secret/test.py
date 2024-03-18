import os
import shutil
from git import Repo


class GitHandler:
    def __init__(self, repo_url, destination_path, gitlab_access_token):
        self.repo_url = repo_url
        self.destination_path = destination_path
        self.gitlab_access_token = gitlab_access_token

    def clone_or_pull_repository(self):
        """
        Clone the Git repository if it doesn't exist locally, or pull changes if it does.
        """
        if not os.path.exists(self.destination_path):
            print("clone repository")
            Repo.clone_from(self.repo_url, self.destination_path)
        else:
            print("pull repository")
            repo = Repo(self.destination_path)
            origin = repo.remote()
            origin.pull()

    def commit_and_push_changes(self, commit_message, target_branch):
        """
        Commit changes and push them to a remote repository.
        :param commit_message: Message for the commit.
        :param target_branch: Name of the branch to push changes.
        """
        repo = Repo(self.destination_path)
        print(f"{repo=}")
    
        # Add all changes to the index, including untracked files
        repo.git.add("--all")
    
        # Check if there are changes to commit
        if not repo.is_dirty():
            print("No changes to commit.")
            return
    
        # Commit changes
        repo.index.commit(commit_message)
    
        # Push changes to remote repository with access token in URL
        origin_url = repo.remote().url
        print("/*" * 20)
        print(f"{origin_url=}")
        print("/*" * 20)
        new_origin_url = (
            origin_url.replace(
                "https://", f"https://oauth2:{self.gitlab_access_token}@"
            )
            if "oauth2" not in origin_url
            else origin_url
        )
        repo.remote().set_url(new_origin_url)
        origin = repo.remote(name="origin")
        try:
            origin.push(refspec=f"{target_branch}:{target_branch}")
            print("Push successful.")
        except GitCommandError as e:
            print("Error occurred during push operation:", e)



    def add_file(self, file_path, content=""):
        """
        Add a file to the repository.
        :param file_path: Path of the file to add.
        :param content: Content of the file (optional).
        """
        full_path = os.path.join(self.destination_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as file:
            file.write(content)

    def delete_file(self, file_path):
        """
        Delete a file from the repository.
        :param file_path: Path of the file to delete.
        """
        full_path = os.path.join(self.destination_path, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        else:
            print(f"File '{file_path}' does not exist.")

    def add_folder(self, folder_path):
        """
        Add a folder to the repository.
        :param folder_path: Path of the folder to add.
        """
        os.makedirs(os.path.join(self.destination_path, folder_path), exist_ok=True)

    def delete_folder(self, folder_path):
        """
        Delete a folder from the repository.
        :param folder_path: Path of the folder to delete.
        """
        folder_to_delete = os.path.join(self.destination_path, folder_path)
        if os.path.exists(folder_to_delete):
            shutil.rmtree(folder_to_delete)
        else:
            print(f"Folder '{folder_path}' does not exist.")


# Example usage
if __name__ == "__main__":
    repo_url = "https://gitlab.com/ssp19960710/0902.git"
    destination_path = "Result/"
    commit_message = "Update via GitPython"
    branch_name = "main"  # Or any branch you want to push to
    gitlab_access_token = "glpat-Jj8d4tBQ_aYyBnfzY498"

    # Instantiate GitHandler
    git_handler = GitHandler(repo_url, destination_path, gitlab_access_token)

    # Clone repository
    git_handler.clone_or_pull_repository()

    # Add a new file
    git_handler.add_file("src/new_file.txt", "This is a new file.")

    # Make changes to the cloned repository (not shown here)

    # Commit and push changes
    git_handler.commit_and_push_changes(commit_message, branch_name)

    # Delete a file
    # git_handler.delete_file("src/new_file.txt")
    # git_handler.delete_folder("src")
