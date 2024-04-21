from gitlabs import FileInfo, GitlabManager

# Example usage:
if __name__ == "__main__":
    token = "glpat--NiKM9WX11AhUHzcffFc"
    project_id = "29301882"
    gitlab_manager = GitlabManager(
        token=token, base_url="https://gitlab.com", project_id=project_id
    )
    # Usage examples

    file_path = "switch_status"
    # res = gitlab_manager.judge_file_or_folder_exist(path=file_path)
    # res = gitlab_manager.judge_file_or_folder_exist(path=file_path,branch="test")
    res = gitlab_manager.get_all_files_path_in_folder(folder_path=file_path)
    print(f"{res=}")

    for item in res:
        content = gitlab_manager.get_file(path=item)
        print(f"{item=} {content=}")

    files = [
        FileInfo(
            file_path="src_100/new_file.txt", content="Content of file 1"
        ),
        FileInfo(
            file_path="src_100/new_file_1.txt", content="Content of file 2"
        ),
        FileInfo(
            file_path="src_100/switch_status/F12P1/golden_config",
            content="Content of file 100",
        ),
        FileInfo(
            file_path="src_100/switch_status/F12P8/golden_config",
            content="Content of file 101",
        ),
        # Add more files as needed
    ]

    commit_message = "Committing multiple files"

    success = gitlab_manager.commit_files_to_gitlab(files, commit_message)
    print(f"commit method result: {success}")

    delete = gitlab_manager.delete_file_on_gitlab(
        "file1.txt", commit_message="delete"
    )
    # delete = gitlab_manager.delete_file_on_gitlab("folder/file2.txt",commit_message="delete")

    # delete=gitlab_manager.delete_folder_on_gitlab("src_120/switch_status",commit_message="delete")
    print(f"delete method result: {delete}")