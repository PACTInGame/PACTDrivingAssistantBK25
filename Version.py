import requests


def get_github_version(owner, repo, file_path):
    url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}'

    response = requests.get(url)

    if response.status_code == 200:
        version = response.text.strip()
        return version

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
        else:
            print("No update available")
        return version
    else:
        print('Failed to retrieve version information.')
        return "0.0.0"



if __name__ == '__main__':
    get_current_version()
