from bs4 import BeautifulSoup

def remake_one(msg, user):
    name = msg.next
    time = msg.next.next.next
    text = msg.next_sibling

    # remake user
    msg.clear()
    msg.string = name.text + ' ' + time.text
    del msg['style']
    msg['class'] = user

    # remake msg
    if text.img is None:
        text_msg = text.text
        text.clear()
        text.string = text_msg
    del text['style']
    text['class'] = 'msg'

def clean_style(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    style_node = soup.head.style
    style_node.string = "body{font-size:12px; line-height:22px; margin:2px;display:left;height: 100vh;}td{font-size:12px; line-height:22px;}"
    style_node.string += "\n.msg{padding-left:20px;font-size:10pt;font-family:'宋体','MS Sans Serif',sans-serif;}"
    style_node.string += "\n.user_a{color:#42B475;padding-left:10px;}"
    style_node.string += "\n.user_b{color:#006EFE;padding-left:10px;}"
    style_node.string += """\n.sidebar {
            position: fixed;
            top: 0;
            left: 0;
            width: 200px;
            height: 100vh;
            background-color: #f4f4f4;
            padding: 15px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            overflow-y: auto;
        }
        .sidebar a {
            width: 200px;
            text-decoration: none;
            color: #333;
            display: block;
            padding: 5px;
            margin-bottom: 5px;
            border-radius: 4px;
        }
        .sidebar a:hover {
            background-color: #ddd;
        }
        img {
            max-width: 800px;
        }
        .section {
            scroll-margin-left: 240px; /* 确保跳转时不被侧边栏遮挡 */
        }
        .content {
            margin-left: 220px;
            flex-grow: 1;
            padding: 20px;
        }"""

    table=soup.find('table')
    table['class'] = 'content'

    sidebar_node = soup.new_tag('div')
    sidebar_node['class'] = 'sidebar'

    cat = soup.new_tag('h3')
    cat.string = "目录"
    sidebar_node.append(cat)
    table.insert_before(sidebar_node)

    for i, tr in enumerate(table.find_all('tr')):
        if tr.text.startswith('日期'):
            tr['id'] = f'sec{i}'
            tr['class'] = 'section'
            sec = soup.new_tag('a')
            sec.string = tr.text
            sec['href'] = f'#sec{i}'
            sidebar_node.append(sec)

        msg = tr.find('div', style='color:#42B475;padding-left:10px;')
        if msg is not None:
            remake_one(msg, 'user_a')

        msg = tr.find('div', style='color:#006EFE;padding-left:10px;')
        if msg is not None:
            remake_one(msg, 'user_b')

    return soup.prettify()

if __name__ == '__main__':
    with open('薛定谔の彩虹猫(228218809)/{0}薛定谔の彩虹猫(228218809)-3.html', 'r') as f:
        html_doc = f.read()
    html_remake = clean_style(html_doc)
    with open('薛定谔の彩虹猫(228218809)/{0}薛定谔の彩虹猫(228218809)-3-clean.html', 'w') as f:
        f.write(html_remake)