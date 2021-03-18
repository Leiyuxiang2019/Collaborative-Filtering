
#定义几种距离计算函数
#更高效的方式为把得分向量化之后使用scipy中定义的distance方法
from math import sqrt


def ReadData(file, data):
   for line in file:
     line = line.strip('\n')
     linelist = line.split(",")
     features=linelist[2].split('|')
     for feature in features:
         if linelist[0] in data:
             data[linelist[0]].update({feature: 1})
         else:
             data[linelist[0]] = {feature: 1}


def ReadData1(file, data):
   for line in file:
     line = line.strip('\n')
     linelist = line.split(",")
     if linelist[0] in data:
         data[linelist[0]].update({linelist[1]:float(linelist[2])})
     else:
         data[linelist[0]]={linelist[1]:float(linelist[2])}

def cos_dis(rating1, rating2):

    distance = 0
    dot_product_1 = 0
    dot_product_2 = 0
    commonRatings = False

    for score in rating1.values():
        dot_product_1 += score^2
    for score in rating2.values():
        dot_product_2 += score^2

    for key in rating1:
        if key in rating2:
            distance += rating1[key] * rating2[key]
            commonRatings = True
    #两个打分序列之间有公共打分电影
    if commonRatings:
        return 1-distance/sqrt(dot_product_1*dot_product_2)
    #无公共打分电影
    else:
        return -1

def pearson_dis(rating1, rating2):

    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    # now compute denominator
    if n==0:
        denominator=0
    else:
        denominator = (sum_x2 - pow(sum_x, 2) / n) * (sum_y2 - pow(sum_y, 2) / n)
        denominator = sqrt(denominator)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator

#查找最近邻
def computesims(keys,moviename,movies):

     sims = {}
     for key in keys:
         if key != moviename:
             sim = cos_dis(movies[key], movies[moviename])
             if sim>0:
              sims.update({key: sim})

     return sims

 #推荐
def recommend(username, test,train,k,movies,n,hash1,hash2,hash3,hash4,hash5):

     # 找到最近邻
     sum=0
     simsum=0
     score={}
     ke=0
     for i in hash1:
         if i in movies:
             simsum=0
     for moviename in movies:
         if moviename not in train[username]:
           sims = computesims(train[username].keys(), moviename ,movies)
           for sim_movie in sims:
               sum=sum+train[username][sim_movie]*sims[sim_movie]
               simsum=simsum+sims[sim_movie]
           score.update({moviename : sum/simsum})
     sse = 0
     if username in test:
         for movie in test[username]:
             sse=sse+abs(test[username][movie]-score[movie])
     for i in hash2:
         if i in movies:
             simsum=1
     score = sorted(score.items(), key=lambda x: x[1], reverse=True)
     l = []
     for i in range(n):
         l.append(score[i][0])
     print(username + '推荐为:')
     print(l)
     return sse

if __name__ == '__main__':
    test = {}
    train = {}
    jug = {}
    file1 = open('movies.csv')
    movies={}
    ReadData(file1, movies)
    file1 = open('test_set.csv')
    file2 = open('train_set.csv')
    file3 = open('ratings.csv')
    ReadData1(file1, test)
    ReadData1(file2, train)
    ReadData1(file3, jug)
    # print(movies)
    # print(train)
    sse=0
    hash1=movies['542'].keys()
    hash2=movies['523'].keys()
    hash3=movies['590'].keys()
    hash4=movies['1903'].keys()
    hash5=movies['824'].keys()
    print(hash1)
    print(hash2)
    print(hash3)
    print(hash4)
    print(hash5)
    for username in test:
           sse=sse+recommend(username, test, train, 10, movies, 10, hash1, hash2, hash3, hash4, hash5)
    print(sse)



