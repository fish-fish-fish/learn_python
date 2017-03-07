# [Beautiful Soup 4.4.0 文档](http://beautifulsoup.readthedocs.io/zh_CN/latest/#descendants)
## 安装bs4
pip install bs4
## import
from bs4 import BeautifulSoup
## 快速开始
from bs4 import BeautifulSoup    
html_doc = '''<head><title>The Dormouse's story</title></head>'''
soup = BeautifulSoup(html_doc, 'html.parser')    //创建BeautifulSoup对象，使用解析器html.parser
print(soup.prettify())    //格式化
## 对象种类：BeautifulSoup, Tag , NavigableString , BeautifulSoup , Comment.
### BeautifulSoup
* BeautifulSoup 对象表示的是一个文档的全部内容.大部分时候,可以把它当作 Tag 对象,它支持 遍历文档树 和 搜索文档树 中描述的大部分的方法.
* 因为 BeautifulSoup 对象并不是真正的HTML或XML的tag,所以它没有name和attribute属性.但soup.name == 'document'
### Tag -- Tag对象与XML或HTML原生文档中的tag相同
`soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')`    
`tag = soup`

* Class : type(tag) == **'bs4.element.Tag'**
* Name :  tag.name == 'b' 获取标签的名字
* Attributes : tag["class"] == 'boldest' 获取标签中国年的属性
* string : 当标签中只有一个字符串时返回该字符串 **(bs4.element.NavigableString)**，有多个时，返回None
* strings: 标签中的文本生成器 type(tag.strings) == **generator**

## 部分函数详解
### find_all() 通过对标签的名字进行筛选
* 字符串：soup.find_all('b') --> 查找文档中所有的`<b>`标签
* 正则表达式: soup.find_all(re.compile("^b")) --> 使用正则表达式筛选
* 列表: soup.find_all(["a", "b"]) --> 文档中所有`<a>`标签和`<b>`标签
* 方法: 自定义过滤函数,def filter(tag) -> bool    
'def has_class_but_no_id(tag):'    
'   return tag.has_attr('class') and not tag.has_attr('id')'    
'soup.find_all(**has_class_but_no_id**)'    
* True: soup.find_all(True) --> 找到所有的tag
* find_all( name , attrs , recursive , string , **kwargs )参数解析
    1. name:tag的名字，可以是**字符串、正则表达式、方法、列表、True**    
soup.find_all("title")
    2. keyword:**如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索**    
    **搜索指定名字的属性时可以使用的参数值包括 *字符串 , 正则表达式 , 列表, True* .**   
    **tag中的*class*属性，在python 中事关键字，使用*class_代替**    
    soup.find_all("a",class_=re.compile(r"sister"))
    soup.find_all(id='link2')    
    soup.find_all(id=True)    id=True 表示只要含有id属性，就返回True
    soup.find_all(href=re.compile("baidu"))    
    3. recursive: 是否递归便利所有标签，默认为True. **如果只想搜索tag的直接子节点,可以使用参数 recursive=False**
    4. string:匹配tag中的文本字符串，同name参数,**string 参数接受 字符串 , 正则表达式 , 列表, True**
    5. limit: 限制搜索返回数量 
* 其他的搜索相关函数使用方法相似

***
### [CSS选择器](http://www.w3.org/TR/CSS2/selector.html) `.select()`  在 **Tag** 或 **BeautifulSoup** 对象的 .select() 方法中传入字符串参数       
* 通过CSS的类名查找:   
soup.select(".sister")  
`[<a class="sister" href="http://example.com/elsie">Elsie</a>`
* 通过tag的id查找:   
soup.select("#link1")
`[<a href="http://example.com/elsie" id="link1">Elsie</a>`      
soup.select("#link1,#link2")        
`[<a href="http://example.com/elsie" id="link1">Elsie</a>`      
`[<a href="http://example.com/elsie" id="link2">Elsie</a>`      
* 通过是否存在某个属性来查找:    
soup.select('a[href]')      
`[<a href="http://example.com/elsie1111" id="link1">Elsie</a>`      
`[<a href="http://example.com/elsie2222" id="link2">Elsie</a>` 
* 通过属性的值来查找:    
soup.select('a[href="http://example.com/elsie1111"]')       
`[<a href="http://example.com/elsie1111" id="link1">Elsie</a>`      
* 可使用CSS选择器的语法找到tag:    
soup.select("title") ---- 查找树中的`<title>`标签      
soup.select("body a") ---- 通过tag标签逐层查找,标签之间可有其他标签       
soup.select("html head title") ---- 通过tag标签逐层查找,标签之间可有其他标签      
* 找到某个tag标签下的直接子标签: **>表示两个tag是直接相邻关系* **       
soup.select("head > title")     
soup.select("head title > p")
* 找到兄弟节点标签: **~**
soup.select("#link1 ~ .sister")  id为link1的tag的兄弟中，选取class为sister的tag
`[<a href="http://example.com/elsie2222" id="link2">Elsie</a>`      
`[<a href="http://example.com/elsie2222" id="link3">Elsie</a>` 


