# finish the function below
import numpy as np
import math
import matplotlib.pyplot as plt

def SolveEquationSet_Gauss(matrix): # matrix is the Coefficient Matrix with Constant Term in numpy.array format.
    row, column = matrix.shape
    #用第i行去消第j行
    for i in range(row):
        matrix[i][-1] = -matrix[i][-1]
    for i in range(row):
        flag = True
        if matrix[i][i] == 0:
            for test in range(i, row):
                if matrix[test][i] != 0:
                    for k in range(column):
                        temp = matrix[test][k]
                        matrix[test][k] = matrix[i][k]
                        matrix[i][k] = temp
                    break
                else:
                    flag = False
        if not flag:
            continue
        
        for k in range(i+1,column):
            matrix[i][k] /= matrix[i][i]
        matrix[i][i] = 1
        for j in range(row):
            if j == i:
                continue
            else:
                for k in range(column-1, -1, -1):
                    matrix[j][k] -= matrix[i][k] * matrix[j][i] 
    if np.linalg.det(matrix[:,0:row]) == 0:
        return -1
    return matrix[:,-1] # the function should return the solution vector in numpy.array format. "None" is just a placeholder here.

def SolveEquationSet_MatMulti(matrix):
    row, column = matrix.shape
    A = matrix[:,0:-1]
    b = -matrix[:,-1]
    D = np.hstack((A, np.eye(row)))
    for i in range(row):
        flag = True
        if D[i][i] == 0:
            for test in range(i, row):
                if D[test][i] != 0:
                    for k in range(row * 2):
                        temp = D[test][k]
                        D[test][k] = D[i][k]
                        D[i][k] = temp
                    break
                else:
                    flag = False
        if not flag:
            continue
        for k in range(i + 1, row * 2):
            D[i][k] /= D[i][i]
        D[i][i] = 1
        for j in range(row):
            if j == i:
                continue
            else:
                for k in range(row*2-1, -1, -1):
                    D[j][k] -= D[i][k] * D[j][i]
    
    result = []
    A = D[:,0:row]
    D = D[:,row:2*row]
    if np.linalg.det(D) == 0 or np.linalg.det(A) == 0:
        return -1
    for i in range(row):
        result.append(b.dot(D[i]))
    x = np.array([y for y in result])
    return x


def memory_Fibanacci(func):
    memory = {}
    def inner(num):
        if num not in memory:
            memory[num] = func(num)
        return memory[num]
    return inner

@memory_Fibanacci           
def solve(num): # this function return the n-th number of Fibonacci
    if num == 0:
        return 0
    if num == 1:
        return 1
    else:
        return solve(num-1) + solve(num-2)

def Fibonacci(query): # query is the list of number you should consider
    result = []
    for n in query:
        result.append(solve(n))
    return result



def skiing(matrix):
    row, column = matrix.shape
    if row + column < 4:
        return -1
    map = np.zeros((row, column))
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    def dp(i, j):
        if map[i][j]:
            return map[i][j]
        for k in range(4):
            if i + dx[k] >= row or i + dx[k] < 0 or j + dy[k] >= column or j + dy[k] < 0:
                continue
            if matrix[i][j] > matrix[i+dx[k]][j+dy[k]]:
                map[i][j] = max(map[i][j], dp(i+dx[k], j+dy[k]) + 1)           
        return map[i][j]
    
    for i in range(row):
        for j in range(column):
            dp(i, j)
    map = np.sort(map.ravel())
    return int(map[-1] + map[-2] + map[-3] + map[-4])

def func_draw():
    l = 0.6
    a = 1
    n = 500000
    k = 0
    g = np.random.uniform(0, a / 2, n)
    theta = np.random.uniform(0 , math.pi, n)

    x = []
    y = []
    for i in range(1, n):
        if g[i] < (l / 2) * math.sin(theta[i]):
            k += 1
        if k >= 1:
            f = k / i
            y.append((2 * l) / (f * a))
            x.append(i)

    plt.plot(x, y)
    plt.hlines(math.pi, 0, n, color="red")
    plt.ylim(3, 3.3)
    plt.title("1700017720")
    plt.savefig("1700017720.png")


# 发布者的基类
import re
class BasePublisher(object):
    
    def __init__(self):
        # BasePublisher 的初始化方法
        # TODO
        self.reader = set()
        self.news = []
        self.type = "Publisher"
    
    def subscribeReader(self, reader):
        # Publisher 端的订阅函数
        # TODO
        self.reader.add(reader)
        
        
    
    def unsubscribeReader(self, reader):
        # Publisher 端的取消订阅函数
        # TODO
        self.reader.remove(reader)
        
        
    def notifyReader(self, new):
        pass
        
    def __str__(self):
        tmpread = []
        for i in self.reader:
            tmpread.append(i.name)
        return "Publisher Name: {}\nSubscribed Reader: {}\nPublisher News: {}".format(self.name, tmpread, self.news)
    
    def get_html(self):
        result = []
        for i in self.news:
            result.append(list(unwrapper(i)))
        size = len(result)
        k = 0
        
        output = ''
        for i in range(size):
            output += '''<p class="{flag0}">{flag1}</p>\n'''.format(flag0=result[i][0],flag1=result[i][1])
        with open("1700017720-%s.html" %(self.name), "w") as file:
            
            index = '''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <style>
                    .red {
                        color:red;
                    }
                    .blue {
                        color:blue;
                    }
                    .green {
                        color:green;
                    }
                    </style>
                        <meta charset="UTF-8">
                        <title>title</title>
                    </head>
                    '''+'''
                    <body>
                        <h1>Type:</h1>
                        <p>{}</p>
                        <h1>Name:</h1>
                        <p>{}</p>
                        <h1>Subscribe Readers:</h1>
                        <p>{}</p>
                        <h1>News:</h1>
                    '''.format(self.type, self.name, [i.name for i in self.reader])+output+'''
                    </body>
                    </html>
                    '''
            file.write(index)
    
# 北大
class PKUPublisher(BasePublisher):
    
    def __init__(self):
        # PKUPublisher 的初始化方法
        # TODO
        BasePublisher.__init__(self)
        self.name = 'PKUPublisher'
        
    def notifyReader(self, new):
        # Publisher 向 Reader 发布消息
        # TODO
        self.news.append(new)
        for i in self.reader:
            i.receiveNew(self, new)
      
        
# 清华
class THUPublisher(BasePublisher):
    
    def __init__(self):
        # THUPublisher 的初始化方法
        # TODO
        BasePublisher.__init__(self)
        self.name = 'THUPublisher'
        
    def notifyReader(self, new):
        # Publisher 向 Reader 发布消息
        # TODO
        self.news.append(new)
        for i in self.reader:
            i.receiveNew(self, new)
        
            
# 人大
class RUCPublisher(BasePublisher):
    
    def __init__(self):
        # RUCPublisher 的初始化方法
        # TODO
        BasePublisher.__init__(self) 
        self.name = 'RUCPublisher'
        
    def notifyReader(self, new):
        # Publisher 向 Reader 发布消息
        # TODO
        self.news.append(new)
        for i in self.reader:
            i.receiveNew(self, new)    


# 读者基类
class BaseReader(object):
    
    def __init__(self):
        # BaseReader 的初始化方法
        # TODO
        self.publisher = set()    
    
    def subscribeToPublisher(self, publisher):
        # Reader向Publisher订阅
        # TODO
        publisher.subscribeReader(self)
          
    def unsubscribeToPublisher(self, publisher):
        # Reader向Publisher取消订阅
        # TODO
        publisher.unsubscribeReader(self)
           
    def receiveNew(self, publisher, new):
        pass
    
    def get_html(self):
        result = []
        for i in self.news:
            result.append(list(unwrapper(i)))
        
        size = len(result)
        k = 0
        output = ''
        for i in range(size):
            output += '''<p class="{flag0}">{flag1}</p>\n'''.format(flag0=result[i][0],flag1=result[i][1])
        with open("1700017720-%s.html" %(self.name), "w") as file:
            
            index = '''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <style>
                    .red {
                        color:red;
                    }
                    .blue {
                        color:blue;
                    }
                    .green {
                        color:green;
                    }
                    </style>
                        <meta charset="UTF-8">
                        <title>title</title>
                    </head>
                    '''+'''
                    <body>
                        <h1>Type:</h1>
                        <p>{}</p>
                        <h1>Name:</h1>
                        <p>{}</p>
                        <h1>Subscribe Publishers:</h1>
                        <p>{}</p>
                        <h1>News:</h1>
                    '''.format(self.type, self.name, self.publisher)+output+'''
                    </body>
                    </html>
                    '''
            file.write(index)
        
    

# 第一种读者
class ReaderType1(BaseReader):
    
    def __init__(self, _name):
        # TODO
        BaseReader.__init__(self)
        self.name = _name
        self.news = []
        self.type = "ReaderType1"
    def subscribeToPublisher(self, publisher):
        # Reader向Publisher订阅
        # TODO
        publisher.subscribeReader(self)
        self.publisher.add(publisher.name)
        
    def receiveNew(self, publisher, new):
        # Reader 从 Publisher 接收消息
        # TODO
        self.news.append(new)
        
    #def __str__(self):
        #listForPrint = set()
        #for key, value in self.news.items():
            #listForPrint.add(key+':'+str(value))
        #return "Reader Name: {}\nSubscribed Publisher: {}\nReader News: {}".format(self.name, list(self.publisher), listForPrint)
        


# 第二种读者
class ReaderType2(BaseReader):
    
    def __init__(self, _name):
        # TODO
        BaseReader.__init__(self)
        self.name = _name
        self.news = []
        self.type = "ReaderType2"
    def subscribeToPublisher(self, publisher):
        # Reader向Publisher订阅
        # TODO
        publisher.subscribeReader(self)
        self.publisher.add(publisher.name)
        
    def receiveNew(self, publisher, new):
        # TODO
        self.news.append(new) 
        
    def __str__(self):
        return "Reader Name: {}\nSubscirbed Publisher: {}\nReader News: {}".format(self.name, list(self.publisher), self.news)         

    
        
def wrapper(tp, msg):
    # TODO wrap the msg into <tp><msg>, please use string.format
    return str("<%d><%s>" %(tp, msg))
def unwrapper(msg):
    # TODO: unwrap the msg and return the type and content. please use regex here
    regex = r'<(\d)><(.*?)>'
    m = re.match(regex, msg)
    return m.group(1).replace('0', 'red').replace('1', 'blue').replace('2', 'green'), m.group(2)


# 创建三个发布者对象
pkuPublisher = PKUPublisher()
thuPublisher = THUPublisher()
rucPublisher = RUCPublisher()

# 创建三位读者，alice 和 bob 为 第一类， tom 为 第二类
alice = ReaderType1('alice')
bob = ReaderType1('bob')
carol = ReaderType2('carol')

# alice 订阅了 pku， thu
alice.subscribeToPublisher(pkuPublisher)
alice.subscribeToPublisher(thuPublisher)

# bob 订阅了 thu， ruc
bob.subscribeToPublisher(thuPublisher)
bob.subscribeToPublisher(rucPublisher)

# tom 订阅了 pku， thu， ruc
carol.subscribeToPublisher(pkuPublisher)
carol.subscribeToPublisher(thuPublisher)
carol.subscribeToPublisher(rucPublisher)

# 发布者发布新消息 通知(00)、新闻(01)、学术(10)
pkuPublisher.notifyReader(wrapper(0, "PKU通知"))
pkuPublisher.notifyReader(wrapper(1, "PKU新闻"))
pkuPublisher.notifyReader(wrapper(2, "PKU学术"))

thuPublisher.notifyReader(wrapper(0, "THU通知"))
thuPublisher.notifyReader(wrapper(1, "THU新闻"))
thuPublisher.notifyReader(wrapper(2, "THU学术"))

rucPublisher.notifyReader(wrapper(0, "RUC通知"))
rucPublisher.notifyReader(wrapper(1, "RUC新闻"))
rucPublisher.notifyReader(wrapper(2, "RUC学术"))

pkuPublisher.get_html()
thuPublisher.get_html()
rucPublisher.get_html()
##
alice.get_html()
bob.get_html()
carol.get_html()



    
    
