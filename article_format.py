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
        raw.encoding = 'utf8'
        content = raw.text
        if content.find('<section') == -1:
            content = content[content.find('<h1')+1:]
            h1 = '<h1>' + content[content.find('>')+1:content.find('<')] + '</h1><br>\n'
            content = content[content.find('<h2')+1:]
            h2 = '<h2>' + content[content.find('>')+1:content.find('<')] + '</h2><br>\n'
            html += h1 + h2 + '<hr>'
            while content.find('<img ') != -1 or content.find('<div class="article-text') != -1:
                if content.find('<img ') == -1:
                    content = content[content.find('<div class="article-text'):]
                    html += content[:content.find('</div>')+6] + '<br>'
                    content = content[content.find('</div>')+6:]
                elif content.find('<div class="article-text') == -1:
                    content = content[content.find('<img '):]
                    html += '<div class="mdui-container">' + imgZoom(content[:content.find('/>')+2]) + '</div>' + '<br>'
                    content = content[content.find('/>')+2:]
                elif content.find('<div class="article-text') < content.find('<img '):
                    content = content[content.find('<div class="article-text'):]
                    html += content[:content.find('</div>')+6] + '<br>'
                    content = content[content.find('</div>')+6:]
                else:
                    content = content[content.find('<img '):]
                    html += '<div class="mdui-container">' + imgZoom(content[:content.find('/>')+2]) + '</div>' + '<br>'
                    content = content[content.find('/>')+2:]
        else:
            content = content[content.find('<section'):content.rfind('</section>')]
            head = content[:content.find('</section>')+10]
            html += head + '\n<hr>'
            while content.find('<img ') != -1 or content.find('<p ') != -1:
                if content.find('<img ') == -1:
                    html += content[content.find('<p '):content.find('</p>')+3] + '<br>'
                    content = content[content.find('</p>')+4:]
                elif content.find('<p ') == -1:
                    content = content[content.find('<img '):]
                    html += '<div class="mdui-container">' + imgZoom(content[:content.find('/>')+2]) + '</div>' + '<br>'
                    content = content[content.find('/>')+2:]
                elif content.find('<p ') < content.find('<img '):
                    html += content[content.find('<p '):content.find('</p>')+3] + '<br>'
                    content = content[content.find('</p>')+4:]
                else:
                    content = content[content.find('<img '):]
                    html += '<div class="mdui-container">' + imgZoom(content[:content.find('/>')+2]) + '</div>' + '<br>'
                    content = content[content.find('/>')+2:]

        # print(content)

        with open('home_suf.html') as f:
            html += ''.join(f.readlines())
        
        with open('./archive/' + uri[uri.rfind('/')+1:] + '.html', 'w', encoding='utf16') as f:
            print(html, file = f)
        return 0
    
    except:
        return 1


if __name__ == '__main__':
    print(mark('https://www.economist.com/interactive/business/2023/01/14/investments-in-ports-foretell-the-future-of-global-commerce'))
