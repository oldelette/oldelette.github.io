from typing import List

import gitlab


class GitlabFileManager:
    def __init__(self, personal_access_token, project_id):
        self.gl = gitlab.Gitlab(
            "https://gitlab.com", private_token=personal_access_token
        )
        self.project = self.gl.projects.get(project_id)

    def get_files_in_folder(self, folder_path):

        def recursive_get_files(files, path):
            file_paths = []
            for file_item in files:
                if file_item["type"] == "blob":
                    file_paths.append(f"{path}/{file_item['path']}")
                elif file_item["type"] == "tree":
                    subfolder_files = self.project.repository_tree(
                        path=file_item["path"], all=True
                    )
                    file_paths.extend(
                        recursive_get_files(
                            subfolder_files, f"{path}/{file_item['path']}"
                        )
                    )
            return file_paths

        files = self.project.repository_tree(path=folder_path, all=True)

        return recursive_get_files(files, folder_path)

    def delete_file(self, file_path, commit_message, branch_name="main"):
        try:
            self.project.files.delete(
                file_path=file_path, branch=branch_name, commit_message=commit_message
            )
            print(f"File '{file_path}' deleted successfully.")
        except gitlab.exceptions.GitlabDeleteError as e:
            print(f"Error deleting file '{file_path}': {e}")

    def delete_folder(
        self, folder_path: str, commit_message: str, branch_name: str = "main"
    ) -> None:
        """
        Deletes a folder and its contents from the GitLab repository.

        Args:
            folder_path (str): The path of the folder to be deleted.
            commit_message (str): The commit message for the deletion.
            branch_name (str, optional): The name of the branch. Defaults to "main".
        """
        try:
            files = self.get_files_in_folder_recursive(folder_path)
            if not files:
                print(f"Folder '{folder_path}' does not exist.")
                return
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Error getting folder '{folder_path}': {e}")
            return

        # Commit the deletion of the folder and its contents
        try:
            actions = [
                {"action": "delete", "file_path": file_path} for file_path in files
            ]
            self.project.commits.create(
                {
                    "branch": branch_name,
                    "commit_message": commit_message,
                    "actions": actions,
                }
            )
            print(
                f"Folder '{folder_path}' and its contents deleted successfully.")
        except gitlab.exceptions.GitlabCreateError as e:
            print(f"Error committing deletion of folder '{folder_path}': {e}")

    def get_files_in_folder_recursive(self, folder_path: str) -> List[str]:
        """
        Recursively retrieves all files and folders within a folder.

        Args:
            folder_path (str): The path of the folder.

        Returns:
            List[str]: A list of file paths.
        """
        files_to_delete: List[str] = []
        try:
            files = self.project.repository_tree(path=folder_path, all=True)
            for file_item in files:
                if isinstance(file_item, dict):  # Check if the item is a dictionary
                    if file_item["type"] == "blob":
                        files_to_delete.append(file_item["path"])
                    elif file_item["type"] == "tree":
                        files_to_delete.extend(
                            self.get_files_in_folder_recursive(
                                file_item["path"])
                        )
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Error getting files in folder '{folder_path}': {e}")
        return files_to_delete


# Example usage
project_id = "29301882"
# personal_access_token = 'glpat-XsaHftC5AtaeoTwHd7nE'
personal_access_token = "glpat--NiKM9WX11AhUHzcffFc"
# file_path = 'path/to/your/file.txt'
# branch_name = 'master'
# commit_message = 'Delete file'
#
git_manager = GitlabFileManager(personal_access_token, project_id)
res = git_manager.get_files_in_folder(folder_path="switch_status")
# print(f"{res=}")
# # Delete a file
# file_path = "bb.txt"
# git_manager.delete_file(file_path, "Delete file")

# Delete a folder
folder_path = "src_9/"
git_manager.delete_folder(folder_path, "Delete folder")
