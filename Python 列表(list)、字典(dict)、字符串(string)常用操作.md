#附：python内置类型
##1、list：列表（即动态数组，C++标准库的vector，但可含不同类型的元素于一个list中）

  a = ["I","you","he","she"]      元素可为任何类型。

###下标：按下标读写，就当作数组处理,以0开始，有负下标的使用
  0第一个元素，-1最后一个元素，
  -len第一个元素，len-1最后一个元素.

###取list的元素数量:                
  len(list)   #list的长度。实际该方法是调用了此对象的__len__(self)方法。 

###创建连续的list
  L = range(1,5)      #即 L=[1,2,3,4],不含最后一个元素
  L = range(1, 10, 2) #即 L=[1, 3, 5, 7, 9]

###list的方法
  L.append(var)   #追加元素
  L.insert(index,var)
  L.pop(var)      #返回最后一个元素，并从list中删除之
  L.remove(var)   #删除第一次出现的该元素
  L.count(var)    #该元素在列表中出现的个数
  L.index(var)    #该元素的位置,无则抛异常 
  L.extend(list)  #追加list，即合并list到L上
  L.sort()        #排序
  L.reverse()     #倒序
  list 操作符:,+,*，关键字del
  a[1:]       #片段操作符，用于子list的提取
  [1,2]+[3,4] #为[1,2,3,4]。同extend()
  [2]*4       #为[2,2,2,2]
  del L[1]    #删除指定下标的元素
  del L[1:3]  #删除指定下标范围的元素
  list的复制
  L1 = L      #L1为L的别名，用C来说就是指针地址相同，对L1操作即对L操作。函数参数就是这样传递的
  L1 = L[:]   #L1为L的克隆，即另一个拷贝。
        
  list comprehension
       [ <expr1> for k in L if <expr2> ]
                
##2、dictionary： 字典（即C++标准库的map）
  dict = {'ob1':'computer', 'ob2':'mouse', 'ob3':'printer'}
  每一个元素是pair，包含key、value两部分。key是Integer或string类型，value 是任意类型。
  键是唯一的，字典只认最后一个赋的键值。

###dictionary的方法
   D.get(key, 0)       #同dict[key]，多了个没有则返回缺省值，0。[]没有则抛异常
   D.has_key(key)      #有该键返回TRUE，否则FALSE
   D.keys()            #返回字典键的列表
   D.values()          #以列表的形式返回字典中的值，返回值的列表中可包含重复元素
   D.items()           #将所有的字典项以列表方式返回，这些列表中的每一项都来自于(键,值),但是项在返回时并没有特殊的顺序         
   D.update(dict2)     #增加合并字典
   D.popitem()         #得到一个pair，并从字典中删除它。已空则抛异常
   D.clear()           #清空字典，同del dict
   D.copy()            #拷贝字典
   D.cmp(dict1,dict2)  #比较字典，(优先级为元素个数、键大小、键值大小)
                    #第一个大返回1，小返回-1，一样返回0
### dict的遍历：
   for (k,v) in D.items:
            
##3、tuple：元组（即常量数组）
   元组中的元素值是不允许修改和删除的。
   tuple = ('a', 'b', 'c', 'd', 'e')
   可以用list的 [],:操作符提取元素。就是不能直接修改元素。

   ###list 和 tuple 的相互转化:

   tuple(ls) 
   list(ls)

###4、string：     字符串（即不能修改的字符list）
   str = "Hello My friend"
   字符串是一个整体。如果你想直接修改字符串的某一部分，是不可能的。但我们能够读出字符串的某一部分。
   子字符串的提取
   str[:6]
   字符串包含判断操作符：in，not in
   "He" in str
   "she" not in str

###string模块，还提供了很多方法，如
  S.find(substring, [start [,end]]) #可指范围查找子串，返回索引值，否则返回-1
  S.rfind(substring,[start [,end]]) #反向查找
  S.index(substring,[start [,end]]) #同find，只是找不到产生ValueError异常
  S.rindex(substring,[start [,end]])#同上反向查找
  S.count(substring,[start [,end]]) #返回找到子串的个数

  S.lowercase()
  S.capitalize()      #首字母大写
  S.lower()           #转小写
  S.upper()           #转大写
  S.swapcase()        #大小写互换

  S.split(str, ' ')   #将string转list，以空格切分
  S.join(list, ' ')   #将list转string，以空格连接

###处理字符串的内置函数
  len(str)                #串长度
  cmp("my friend", str)   #字符串比较。第一个大，返回1
  max('abcxyz')           #寻找字符串中最大的字符
  min('abcxyz')           #寻找字符串中最小的字符

###string的转换
            
  float(str)      #变成浮点数，float("1e-1")  结果为0.1
  int(str)        #变成整型，  int("12")  结果为12
  int(str,base)   #变成base进制整型数，int("11",2) 结果为2

###字符串的格式化（注意其转义字符，大多如C语言的，略）
   str_format % (参数列表) #参数列表是以tuple的形式定义的，即不可运行中改变
   print ""%s's height is %dcm" % ("My brother", 180)
          #结果显示为 My brother's height is 180cm
