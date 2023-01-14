import requests
import article_format

MIRROR = 'https://www.economist.com'

def get(sectionName='', proxy=False, http_proxy='', https_proxy='') -> tuple:
    try:
        if proxy:
            raw = requests.get(f'https://www.economist.com/{sectionName}', proxies={'http': http_proxy, 'https': https_proxy})
        else:
            raw = requests.get(f'https://www.economist.com/{sectionName}')
    except:
        return None #####################################
    raw.encoding = 'utf8'
    content = raw.text
    if not sectionName:
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
        if article_format.mark(link) == 0:
            link = f'archive/{link[link.rfind("/")+1:]}.html'
        h3 = h3[h3.find(">")+1:]
        h3 = h3[h3.find(">")+1:]
        title = h3[:h3.find('</a>')]
        titles.append([title, link])
        content = content[content.find('</h3>')+5:]

        currentDetail.append(content[content.find('<p '):content.find('</p>')])
        currentDetail[2] = currentDetail[2][currentDetail[2].find('>')+1:]
        content = content[content.find('</p>')+4:]

        details.append(currentDetail)

    if not sectionName:
        titles.insert(3, ['The world in brief', 'https://arielherself.github.io/espresso-native'])
        details.insert(3, ['', 'Espresso', 'Catch up quickly on the global stories that matter'])

    # print(titles, '\n\n', details)
    # print(len(titles), len(details))
    assert(len(titles) == len(details))

    return titles, details

def getSection1(sectionName, proxy=False, http_proxy='', https_proxy='') -> tuple:
    try:
        if proxy:
            raw = requests.get(f'https://www.economist.com/{sectionName}', proxies={'http': http_proxy, 'https': https_proxy})
        else:
            raw = requests.get(f'https://www.economist.com/{sectionName}')
    except:
        return None #####################################
    raw.encoding = 'utf8'
    content = raw.text
    content = content[content.find('id="reports-archive"'):]
    
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

        content = content[content.find('<time ')+6:]
        time = content[content.find('>')+1:content.find('<')]
        currentDetail.append(time)

        content = content[content.find('<h2 ')+4:]
        h2 = content[content.find('>')+1:content.find('</h2>')]

        content = content[content.find('<p ')+3:]
        dscp = content[content.find('>')+1:content.find('</p>')]
        currentDetail.append(dscp)

        content = content[content.find('<a ')+3:]
        content = content[content.find('href="')+6:]
        link = content[:content.find('"')]
        if article_format.mark(link) == 0:
            link = f'archive/{link[link.rfind("/")+1:]}.html'

        titles.append([h2, link])
        details.append(currentDetail)

    # print(titles, '\n\n', details)
    # print(len(titles), len(details))
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

    with open('home_suf.html') as f:
        sf = ''.join(f.readlines())
    html += sf

    return html

def sectionGet(sectionName=''):
    print(f'Processing {sectionName if sectionName else "index"} ...')
    try:
        html = layout(makeCell(*get(sectionName)))
        with open(f'{sectionName if sectionName else "index"}.html', 'w', encoding='utf8') as f:
            print(html, file = f)
        return 0
    except:
        return 1

def section1Get(sectionName=''):
    print(f'Processing {sectionName if sectionName else "index"} ...')
    try:
        html = layout(makeCell(*getSection1(sectionName)))
        with open(f'{sectionName}.html', 'w', encoding='utf8') as f:
            print(html, file = f)
        return 0
    except:
        return 1

if __name__ == '__main__':
    sections = ('', 'leaders', 'letters', 'briefing', 'united-states', 'the-americas',
                'asia', 'china', 'middle-east-and-africa', 'europe', 'britain', 'international',
                'business', 'finance-and-economics', 'science-and-technology', 'culture',
                'graphic-detail', 'obituary', 'essay')
    section1s = ('special-reports', 'technology-quarterly')

    for section in sections:
        while sectionGet(section) == 1: pass

    for section in section1s:
        while section1Get(section) == 1: pass
