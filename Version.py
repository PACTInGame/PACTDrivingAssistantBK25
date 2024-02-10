import requests


def get_github_version(owner, repo, file_path):
    url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}'
    try:
        response = requests.get(url)

        if response.status_code == 200:
            version = response.text.strip()
            return version
    except:
        "It seems like there is internet issue! Starting without version check."
    # Return None if the version file couldn't be retrieved
    return None


def get_current_version(current_version):
    # Usage example
    owner = 'PACTInGame'
    repo = 'PACTDrivingAssistantBK25'
    file_path = 'version.txt'

    version = get_github_version(owner, repo, file_path)
    if version:
        version = str(version)
        version = version.split('= ')[1]
        if current_version != version:
            print("Current version: " + current_version)
            print("Update available to version: " + version)
            return True
        else:
            print("No update available")
            return False
    else:
        print('Failed to retrieve version information.')
        return False

