from BeautifulSoup import BeautifulSoup, NavigableString, Comment
import re


def strip_tags(soup, valid_tags):
  #html = re.sub('</scr', '<\/scr', html)
  #soup = BeautifulSoup(html)
  
  for tag in soup.findAll(True):
    if tag.name not in valid_tags:
        tag.replaceWith(tag.renderContents())

  return soup


f = open('weeklyworld')
html = f.read()
#html = re.sub('</scr', '<\/scr', html)
invalid_blocks = ['script', 'noscript']
valid_tags = ['p','div']
soup = BeautifulSoup(html)
for tag in invalid_blocks:
  [z.extract() for z in soup(tag)]
for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
  comment.extract()
  
#print soup
#print strip_tags(soup, valid_tags)

divs = soup.findAll('div')
for d in divs:
  if d.has_key('class'):
      if d['class'] == 'content':
          print d
