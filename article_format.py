import requests

def imgZoom(html: str) -> str:
    while True:
        if html.find('sizes=') != -1:
            a = html[:html.find('sizes=')]
            b = html[html.find('sizes=')+8:]
            b = b[b.find('"')+1:]
            html = a + b
        elif html.find('style=') != -1:
            a = html[:html.find('style=')]
            b = html[html.find('style=')+8:]
            b = b[b.find('"')+1:]
            html = a + b
        elif html.find('width=') != -1:
            a = html[:html.find('width=')]
            b = html[html.find('width=')+8:]
            b = b[b.find('"')+1:]
            html = a + b
        elif html.find('height=') != -1:
            a = html[:html.find('height=')]
            b = html[html.find('height=')+9:]
            b = b[b.find('"')+1:]
            html = a + b
        else:
            break
    return html

def mark(uri: str) -> int:      # return an error code.
    try:
        html = ''
        with open('article_template.html') as f:
            html += ''.join(f.readlines())
        raw = requests.get(uri)
        content = raw.text
        
        content = content[content.find('<section'):content.find('"ufinish"')]
        head = content[:content.find('</section>')+10]
        html += head + '\n'

        while content.find('<img ') != -1 or content.find('<p ') != -1:
            if content.find('<img ') == -1:
                html += content[content.find('<p '):content.find('</p>')+4]
                content = content[content.find('</p>')+5:]
            elif content.find('<p') == -1:
                content = content[content.find('<img '):]
                html += '<div class="mdui-container">' + imgZoom(content[:content.find('/>')+2]) + '</div>'
                content = content[content.find('/>')+3:]
            elif content.find('<p') < content.find('<img '):
                html += content[content.find('<p '):content.find('</p>')+4]
                content = content[content.find('</p>')+5:]
            else:
                content = content[content.find('<img '):]
                html += '<div class="mdui-container">' + imgZoom(content[:content.find('/>')+2]) + '</div>'
                content = content[content.find('/>')+3:]

        with open('home_suf.html') as f:
            html += ''.join(f.readlines())
        
        with open('./archive/' + uri[uri.rfind('/')+1:] + '.html', 'w', encoding='utf8') as f:
            print(html, file = f)
        return 0
    
    except:
        return 1


if __name__ == '__main__':
    print(mark('https://www.economist.com/essay/2022/09/08/the-alaskan-wilderness-reveals-the-past-and-the-future'))
