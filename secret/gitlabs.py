"""GitlabManager to manage interactions with GitLab."""

from typing import List, Optional

from gitlab import Gitlab, GitlabError
from pydantic import BaseModel


class FileInfo(BaseModel):
    """
    Represents information about a file.

    Attributes:
        file_path (str): The path of the file.
        content (str): The content of the file.
    """

    file_path: str
    content: str


class GitlabManager:
    """
    Args:
        token (str): The GitLab access token.
        base_url (str): The base URL of the GitLab instance.
        project_id (int): The ID of the GitLab project.

    Attributes:
        gl: An instance of Gitlab.
        project: An instance of the GitLab project.
        branch_names (set): A set containing the names of all branches.

    Methods:
        judge_file_or_folder_exist: Checks if a file/folder exists in the repo.
        get_all_files_path_in_folder: Retrieves all file paths in a folder.
        commit_files_to_gitlab: Commits changes to GitLab.
        delete_file_on_gitlab: Deletes a file from GitLab.
        delete_folder_on_gitlab: Deletes a folder and its contents from GitLab.
    """

    def __init__(self, token: str, base_url: str, project_id: int):
        self.gl = Gitlab(base_url, private_token=token)
        self.project = self.gl.projects.get(project_id)
        self.branch_names = {
            branch.name for branch in self.project.branches.list()
        }

    def _validate_path(self, path: str):
        if not path:
            raise ValueError("Path cannot be empty")

    def _validate_branch(self, branch: str):
        if branch not in self.branch_names:
            raise ValueError(
                f"Branch '{branch}' does not exist in the project"
            )

    def get_file(self, path: str, branch: str = "main") -> Optional[str]:
        """
        Retrieves the content of a file.

        Args:
            path (str): The path of the file.
            branch (str, optional): The branch name. Defaults to main.

        Returns:
            Optional[str]: The content of the file,
            or None if the file is not found.
        """
        try:
            return (
                self.project.files.get(file_path=path, ref=branch)
                .decode()
                .decode()
            )
        except GitlabError as e:
            print(f"Error retrieving file {path}: {e}")
            return None

    def _check_content_match(
        self, existing_content: str, new_content: str
    ) -> bool:
        return existing_content is not None and existing_content == new_content

    def judge_file_or_folder_exist(
        self, path: str, branch: str = "main"
    ) -> bool:
        """
        Checks if a file or folder exists in the repository.

        Args:
            path (str): The path of the file or folder.
            branch (str, optional): The branch name. Defaults to "main".

        Returns:
            bool: True if the file or folder exists, False otherwise.
        """
        self._validate_path(path)
        self._validate_branch(branch)

        try:
            self.project.files.get(file_path=path, ref=branch)
            return True
        except GitlabError:
            pass

        try:
            self.project.repository_tree(path=path, ref_name=branch)
            return True
        except GitlabError:
            return False

    def get_all_files_path_in_folder(
        self, folder_path: str = "", branch: str = "main"
    ) -> List[str]:
        """
        Retrieves all file paths in a folder.

        Args:
            folder_path (str, optional): The path of the folder.
            Defaults to "" (root folder).
            branch (str, optional): The branch name. Defaults to "main".

        Returns:
            List[str]: A list of file paths.
        """
        self._validate_branch(branch)
        all_files = set()

        try:
            # If folder_path is empty, start from the root folder
            if not folder_path:
                folder_path = "/"

            # Retrieve all files under the specified folder
            files = self.project.repository_tree(
                path=folder_path, ref_name=branch, recursive=True, get_all=True
            )

            for file in files:
                if file["type"] == "blob":
                    all_files.add(file["path"])

            # Recursively collect file paths from subfolders
            subfolders = [
                file["path"] for file in files if file.get("type") == "tree"
            ]

            for subfolder in subfolders:
                subfolder_files = self.get_all_files_path_in_folder(
                    subfolder, branch
                )
                all_files.update(subfolder_files)

            return list(all_files)
        except GitlabError as e:
            print(f"Error retrieving files in folder: {e}")
            return []

    def commit_files_to_gitlab(
        self, files: List[FileInfo], commit_message: str, branch: str = "main"
    ) -> bool:
        """
        Commits changes to GitLab.

        Args:
            files (List[FileInfo]): A list of FileInfo obj contain file info
            commit_message (str): The commit message.
            branch (str, optional): The branch name. Defaults to "main".

        Returns:
            bool: True if the commit is successful, False otherwise.
        """
        self._validate_branch(branch)
        actions = []

        try:
            for file_info in files:
                file_path = file_info.file_path
                content = file_info.content
                existing_content = self.get_file(file_path, branch)

                if self._check_content_match(existing_content, content):
                    print(f"Skipping commit for file {file_path}")
                    continue

                actions.append({
                    "action": (
                        "update" if existing_content is not None else "create"
                    ),
                    "file_path": file_path,
                    "content": content,
                })

            if not actions:
                print("No files need to commit.")
            else:
                self.project.commits.create({
                    "actions": actions,
                    "branch": branch,
                    "commit_message": commit_message,
                })
            return True

        except GitlabError as e:
            print(f"Error committing files to GitLab: {e}")
            return False

    def delete_file_on_gitlab(
        self, file_path: str, commit_message: str, branch: str = "main"
    ) -> bool:
        """
        Deletes a file from GitLab.

        Args:
            file_path (str): The path of the file to delete.
            commit_message (str): The commit message for the deletion.
            branch (str, optional): The branch name. Defaults to "main".

        Returns:
            bool: True if the deletion is successful, False otherwise.
        """
        self._validate_path(file_path)
        self._validate_branch(branch)
        if not self.judge_file_or_folder_exist(file_path, branch):
            print(f"File '{file_path}' does not exist.")
            return True

        try:
            self.project.files.delete(
                file_path, branch=branch, commit_message=commit_message
            )
            return True
        except GitlabError as e:
            print(f"Error deleting file on GitLab: {e}")
            return False

    def delete_folder_on_gitlab(
        self, folder_path: str, commit_message: str, branch: str = "main"
    ) -> bool:
        """
        Deletes a folder and its contents from the GitLab repository.

        Args:
            folder_path (str): The path of the folder to be deleted.
            commit_message (str): The commit message for the deletion.
            branch (str, optional): The name of the branch. Defaults to "main".

        Returns:
            bool: True if the deletion is successful, False otherwise.
        """
        self._validate_path(folder_path)
        self._validate_branch(branch)
        if not self.judge_file_or_folder_exist(folder_path, branch):
            print(f"Folder '{folder_path}' does not exist.")
            return True

        try:
            # Retrieve all files within the folder
            files = self.get_all_files_path_in_folder(folder_path, branch)
            print(f"Files ready to delete: {files}")

            # Delete each file within the folder
            actions = [
                {"action": "delete", "file_path": file_path}
                for file_path in files
            ]
            print(f"{actions=}")
            self.project.commits.create({
                "actions": actions,
                "branch": branch,
                "commit_message": commit_message,
            })

            return True
        except GitlabError as e:
            print(f"Error deleting folder on GitLab: {e}")
            return False