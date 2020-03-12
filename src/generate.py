import requests, re, csv, cson, math

list_of_lists = []

with open('src.cson', 'rb') as fin:
    model = cson.load(fin)

with open('algebra_kurosh.cson', 'rb') as fin:
    model['files'] += cson.load(fin)['files']

with open('theme.cson', 'rb') as fin:
    theme = cson.load(fin)


for _file in model['files']:
    with open('../'+_file['name']+'.html', 'wb') as fout:
        fout.write(theme['header'].encode())
        # <!-- Navbar -->
        navbar = theme['navbar']

        tabs = '\n        '.join([navbar[(''if _file['title']==file_['title']else'in')+'active'].format({
                'name' : file_['title']
            ,   'url'  : file_['name']
            }) for file_ in model['files'] if ('pos' in file_.keys() and file_['pos']=='navbar')])
        
        fout.write(navbar['template'].format({'tabs': tabs}).encode())
  
        # <!-- Main content -->
        main_content = theme['main']
        blocks = ''
        pagination = ''
        if 'data' in _file.keys():
            for jdx, data in enumerate(_file['data']):
                
                data_keys = data.keys()
                title     = data['title']     if 'title'     in data_keys else ''
                text      = data['text']      if 'text'      in data_keys else None
                text_     = data['text_']     if 'text_'     in data_keys else None
                small_img = data['small_img'] if 'small_img' in data_keys else None
                big_img   = data['big_img']   if 'big_img'   in data_keys else None

                title = '<a name="subtitle{}"></a>'.format(jdx) + title

                right_subblock = main_content['right_subblock']
                r_subblock = right_subblock['theme'].format({'subblocks': (right_subblock['small'].format(small_img) if small_img else '') + (right_subblock['big'].format(big_img) if big_img else '')})
                
                if 'links' in data_keys:
                    link_template = '    <li><a href="{0[url]}">{0[name]}</a></li>'
                    subt_template = '    <h5>{0[name]}</h5>'
                    
                    text = '<ul style="list-style-type:disc;">\n{}\n<ul>'.format(\
                        '\n'.join([(link_template.format({
                                'name': x['title']
                            ,   'url' : x['url']+'.html'
                            }) if ('url' in x.keys()) else subt_template.format({'name': x['title']})) for x in data['links'] ])) + (text if text else '')
                    list_of_lists.append([x['url'] for x in data['links'] if 'url' in x.keys()])

                if text and not text_:
                    blocks += main_content['block64'].format({
                        'title': title
                    ,   'text': text
                    ,   'subblocks': r_subblock
                    })
                elif text_ and not text:
                    blocks += main_content['block'].format({
                        'title': title
                    ,   'text': text_
                    ,   'subblocks': r_subblock
                    })
                elif text_ and text:
                    blocks += main_content['block64'].format({
                        'title': title
                    ,   'text': text + '\n\n' + text_
                    ,   'subblocks': r_subblock
                    })
        the_list = None
        for _list in list_of_lists:
            if _file['name'] in _list:
                the_list = _list
                break

        if the_list:
            pagination = main_content['pagination']
            S = 7
            Shlf = math.floor(0.5 * float(S))
            idx = the_list.index(_file['name'])
            L = len(the_list)
            start = 0
            end = S

            if 0 > idx - Shlf:
                end = min(L,S)
            elif idx + Shlf + 1 > L:
                start = max(0,L-S)
                end = L
            else:
                start = idx - Shlf
                end = idx + Shlf + 1
            
            pages = '\n        '.join([pagination[('' if x == idx else 'in')+'active'].format({'url':the_list[x], 'num':x}) for x in range(start, end)])
            pagination = pagination['template'].format({'pages': pages})


        # <!-- Sidebar -->
        sidebar = theme['sidebar']
        links = [data['title'] for data in _file['data'] if 'text' not in data.keys()] if 'data' in _file.keys() else None
        
        if links:
            links = '\n'.join(sidebar['link'].format({'url': '#subtitle'+str(idx),'name' : x}) for idx, x in enumerate(links))
            fout.write( ('\n\n' + sidebar['template'].format({'title': 'Разделы', 'links': links})).encode() )
        
        

        fout.write(main_content['template'].format({'blocks': blocks, 'pagination': pagination}).encode())

        fout.write(theme['footer'].encode())
