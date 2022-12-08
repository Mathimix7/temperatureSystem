import onedrivesdk_fork as onedrivesdk

scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
api_base_url='https://api.onedrive.com/v1.0/'

http_provider = onedrivesdk.HttpProvider()
auth_provider = onedrivesdk.AuthProvider(http_provider, scopes=scopes)
client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

client.auth_provider.load_session(path=r'D:\Projects-Python\PythonAPI\onedrive\1drv.session')


def createFile(pathOneDrive, name, filePath):
    client.item(path=pathOneDrive).children[name].upload(filePath)

def downloadFile(pathOneDrive, pathDownload):
    client.item(path=pathOneDrive).download(pathDownload)

def createFolder(name, path="/"):
    i = onedrivesdk.Item()
    i.name = name
    i.folder = onedrivesdk.Folder()
    client.item(path=path).children.add(i)

def renameItem(path, name):
    renamed_item = onedrivesdk.Item()
    renamed_item.name = name
    client.item(path=path).update(renamed_item)