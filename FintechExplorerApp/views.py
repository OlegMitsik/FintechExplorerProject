from django.shortcuts import render

from FintechExplorerApp.models import Load_DB_Taxonomy, Load_RecentCustomRequests, ProcessNewCustomQuery
from FintechExplorerApp.GoogleDrive import ColumbiaFintechFolderID, get_credentials, SearchFolders, SearchFiles
from FintechExplorerApp.Taxonomy import Generate_Taxonomy_JSON

from apiclient import discovery
import httplib2
import socks



def index(request):
    return render(request, 'FintechExplorerApp/Index.html')

def taxonomy(request):
    context = dict()
    context['Taxonomy_JSON'] = Generate_Taxonomy_JSON(Load_DB_Taxonomy())
    return render(request, 'FintechExplorerApp/Taxonomy.html', context)

def select_category(request):

    try:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        FoldersData = SearchFolders(service, ColumbiaFintechFolderID)

    except:
        credentials = get_credentials()
        p = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, 'proxy.server', 3128)
        http = credentials.authorize(httplib2.Http(proxy_info = p))
        service = discovery.build('drive', 'v3', http=http)

        FoldersData = SearchFolders(service, ColumbiaFintechFolderID)

    Categories_arr = []
    folders_rest = []
    ind = 0
    for Folder in FoldersData:
        ind = ind + 1
        if (ind <= 10):
            Categories_arr.append([Folder['name'],Folder['name']])
        else:
            folders_rest.append(Folder['name'])

    Categories_arr.append(["Other reports",folders_rest])
    Categories_arr.append(["Custom search","custom"])

    context = dict()
    context['Categories'] = Categories_arr
    return render(request, 'FintechExplorerApp/Categories.html', context)

def category_selected(request):
    try:
        select_value = request.GET['selected']
    except:
        return render(request, 'FintechExplorerApp/Unauthorized_Request.html')
    else:
        if (select_value == "custom"):
            return custom_search(request)
        else:
            return file_grid(request)

def custom_search(request):
    context = dict()
    context['RecentRequests'] = Load_RecentCustomRequests(5)
    return render(request, 'FintechExplorerApp/Custom_Search.html', context)

def file_grid(request):
    try:
        PageName = ""
        CustomQueryType = ""
        try:
            CustomQueryType = request.GET['CustomQueryType']
        except:
            pass
        CustomQueryName = ""
        CustomQueryContent = ""
        if (CustomQueryType == "name"):
            CustomQueryName = request.GET['custom_search']
            PageName = "Custom Search: " + CustomQueryName
            ProcessNewCustomQuery(CustomQueryName)
        if (CustomQueryType == "content"):
            CustomQueryContent = request.GET['custom_search']
            PageName = "Custom Search: " + CustomQueryContent
            ProcessNewCustomQuery(CustomQueryContent)

        select_value = []
        try:
            select_value.append(request.GET['selected'])
            PageName = select_value[0]
            try:
                select_value = eval(request.GET['selected'])
                PageName = "Other reports"
            except:
                pass
        except:
            pass

        try:
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('drive', 'v3', http=http)

            FoldersData = SearchFolders(service, ColumbiaFintechFolderID)

        except:
            credentials = get_credentials()
            p = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, 'proxy.server', 3128)
            http = credentials.authorize(httplib2.Http(proxy_info = p))
            service = discovery.build('drive', 'v3', http=http)

            FoldersData = SearchFolders(service, ColumbiaFintechFolderID)

        FoldersCleaned = []
        if (select_value):
            for Folder in FoldersData:
                for Selected in select_value:
                    if (Folder['name'] == Selected):
                        FoldersCleaned.append(Folder)
                        break
        elif (CustomQueryType):
            FoldersCleaned = FoldersData

        FileSearchResults = []
        for Folder in FoldersCleaned:
            FileSearchResults = FileSearchResults + SearchFiles(service, Folder['id'], CustomQueryName, CustomQueryContent)

        if (FileSearchResults):
            context = dict()
            context['FileGrid'] = FileSearchResults
            context['PageName'] = PageName
            return render(request, 'FintechExplorerApp/File_grid.html', context)
        else:
            return render(request, 'FintechExplorerApp/Search_no_result.html')

    except:
        return render(request, 'FintechExplorerApp/Unauthorized_Request.html')













