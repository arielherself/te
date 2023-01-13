import requests
import datetime

MIRROR = 'https://www.economist.com'

def get(proxy=False, http_proxy='', https_proxy='') -> tuple:
    try:
        if proxy:
            raw = requests.get('https://www.economist.com', proxies={'http': http_proxy, 'https': https_proxy})
        else:
            raw = requests.get('https://www.economist.com')
    except:
        return None #####################################
    content = raw.text
    content = content[content.find('top-stories'):]
    while content.find('<figure') != -1:
        content = content[:content.find('<figure')] + content[content.find('<figure'):][content[content.find('<figure'):].find('</div>'):]
    
    titles = []     # [title, URI]
    details = []    # [img, section, subTitle]
    while content.find('<p ') != -1:
        currentDetail = []

        if content.find('<img ') != -1 and content.find('<img ') < content.find('<p '):
            imgURI = content[content.find('<img ')+5:]
            imgURI = imgURI[imgURI.find('src="')+5:]
            imgURI = imgURI[:imgURI.find('"')]
            if not imgURI.startswith('data:'):
                currentDetail.append(imgURI)
            else:
                currentDetail.append('')
        else:
            currentDetail.append('')

        if content.find('<p ') < content.find('<h3 '):
            currentDetail.append(content[content.find('<p '):content.find('</p>')])
            currentDetail[1] = currentDetail[1][currentDetail[1].find('>')+1:]
            content = content[content.find('</p>')+4:]
        else:
            currentDetail.append('')

        h3 = content[content.find('<h3 '):content.find('</h3>')]
        link = MIRROR + h3[h3.find('href="')+6:h3[h3.find('href="')+6:].find('"')+h3.find('href="')+6]
        h3 = h3[h3.find(">")+1:]
        h3 = h3[h3.find(">")+1:]
        title = h3[:h3.find('</a>')]
        titles.append([title, link])
        content = content[content.find('</h3>')+5:]

        currentDetail.append(content[content.find('<p '):content.find('</p>')])
        currentDetail[2] = currentDetail[2][currentDetail[2].find('>')+1:]
        content = content[content.find('</p>')+4:]

        details.append(currentDetail)

    titles.insert(3, ['The world in brief', 'https://arielherself.github.io/espresso-native'])
    details.insert(3, ['', 'Espresso', 'Catch up quickly on the global stories that matter'])

    print(titles, '\n\n', details)
    print(len(titles), len(details))
    assert(len(titles) == len(details))

    return titles, details

def makeCell(titles, details) -> list:
    cells = []
    while details[0][0] == '':
        titles = titles[1:]
        details = details[1:]
    for i in range(0, len(titles)):
        cell = ''
        if i % 4 == 0:
            if i != 0:
                cell += f'</div></div>{"<hr>" if i != 4 else ""}\n'
            cell += '<div class="mdui-row">\n'
            cell += '<div class="mdui-col-md-5">\n'
        cell += f'''
        <div class="mdui-row">
<div class="mdui-card" style="cursor: pointer;" onclick="window.open(`{titles[i][1]}`);">
'''
        if i % 4 != 0:
            if details[i][0]:
                cell += f'''
                          <div class="mdui-card-primary">
                          <div class="mdui-row">
                          <div class="mdui-col-xs-9">
        <div class="mdui-card-primary-subtitle">{details[i][1]}</div>
        <div class="mdui-card-primary-title">{titles[i][0]}</div>
        <div class="mdui-card-primary-subtitle">{details[i][2]}</div>
        </div><div class="mdui-col-xs-3">
    <img src="{details[i][0]}"/></div>
    </div>
    </div>
    </div>
    </div>
                '''
            else:
                cell += f'''
                          <div class="mdui-card-primary">
        <div class="mdui-card-primary-subtitle">{details[i][1]}</div>
        <div class="mdui-card-primary-title">{titles[i][0]}</div>
        <div class="mdui-card-primary-subtitle">{details[i][2]}</div>
            </div>
    </div>
    </div>
                '''
            cells.append(cell)
            continue
        if details[i][0]:
            cell += f'''
  <div class="mdui-card-media">
    <img src="{details[i][0]}"/>
          <div class="mdui-card-primary">
        <div class="mdui-card-primary-subtitle">{details[i][1]}</div>
        <div class="mdui-card-primary-title">{titles[i][0]}</div>
        <div class="mdui-card-primary-subtitle">{details[i][2]}</div>
    </div>
  </div>
</div>  
</div>  
'''
        else:
            cell += f'''
  <div class="mdui-card-media">
            <div class="mdui-card-primary">
        <div class="mdui-card-primary-subtitle">{details[i][1]}</div>
        <div class="mdui-card-primary-title">{titles[i][0]}</div>
        <div class="mdui-card-primary-subtitle">{details[i][2]}</div>
      </div>
    </div>
  </div>
</div>  
'''
        if i % 4 == 0:
            cell += '</div><div class="mdui-col-md-7">\n'
        cells.append(cell)

    return cells

def layout(cells) -> str:
    html = ''

    with open('home_template.html') as f:
        pr = ''.join(f.readlines())
    html += pr

    for cell in cells:
        html += cell

    return html

if __name__ == '__main__':
    html = layout(makeCell(*get()))
    with open('index.html', 'w') as f:
        print(html, file = f)
    