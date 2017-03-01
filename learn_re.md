# 正则表达式（python re模块） 学习笔记
***
## special characters:
* '.' : 匹配1个任意字符，换行符(/n)除外
* '^' : 用于标示字符串的开始
* '$' : 用于标示字符串的结束
* '*' : 匹配0个或重复尽可能多的前面的匹配项（贪婪）
* '+' : 匹配1个或重复尽可能多的前面的匹配项（贪婪）
* '?' : 匹配0个或1个前面的匹配项（贪婪）
* '*?,+?,??' : 上面3个符号的非贪婪模式
* {m,n} : 匹配 m -> n 个重复匹配项（贪婪）
* {m,n}？ : 非贪婪模式
* '\\' : 转义特殊字符
* [] :标示一个字符集合
* '|' : A|B, creates an RE that will match either A or B.
***
## special sequences
* \number 匹配一组相同的数字
* \A Matches only at the start of the string.
* \Z Matches only at the end of the string.
* \b Matches the empty string, but only at the start or end of a word.
* \B Matches the empty string, but not at the start or end of a word.
* \d 匹配 十进制数字；等价于［0-9］
* \D 匹配 非十进制数字；等价于[^0-9]. 此处 **^** 表示取反
* \s 匹配任何空白字符；等价于[ \t\n\r\f\v]
* \S 匹配任何非空白字符；等价于[^ \t\n\r\f\v]
* \w Matches any alphanumeric character; equivalent to [a-zA-Z0-9_].
* \W \wd的 补集
* \\ 匹配转义符号
***
## demo
