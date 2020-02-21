import requests, re, csv, cson


with open('src.cson', 'rb') as fin:
    model = cson.load(fin)

with open('theme.cson', 'rb') as fin:
    theme = cson.load(fin)


for _file in model['files']:
    with open(_file['name']+'.html', 'wb') as fout:

        # <!-- Navbar -->
        navbar = theme['navbar']

        tabs = '\n'.join([navbar[(''if _file['title']==file_['title']else'in')+'active'].format({
                'name' : file_['title']
            ,   'url'  : file_['name']
            }) for file_ in model['files']])

        #fout.write(navbar.format({'tabs': tabs}))

        # <!-- Sidebar -->
        sidebar = theme['sidebar']
        links = [data['title'] for data in _file['data'] if 'text' not in data.keys()]\
                    if 'data' in _file.keys() else None

        if links:
            links = '\n'.join(sidebar['link'].format({'url': '#subtitle'+str(idx),'name' : x}) for idx, x in enumerate(links))
            #fout.write( '\n\n' + sidebar['template'].format({'title': 'Разделы', 'links': links}) )
            
        # <!-- Main content -->
        main_content = theme['main']
        blocks = ''
        if 'links' in _file['data'].keys():
            for link in _file['data']['links']:
                _file['data']['links'] # список ссылок и содержимого страниц




        #fout.write(theme['footer'])
