

from math import sqrt


def ReadData(file, data):
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
def computeNearestNeighbor(username, test,train):

     distances = []
     for user in train:
         if user != username:
             #distance = manhattan_dis(users[user], users[username])
             distance = pearson_dis(train[user], train[username])
             distances.append((distance, user))
     # 根据距离排序，距离越近，排得越靠前
     distances.sort(reverse = True)
     return distances

 #推荐
def recommend(username, test,train,k,jug,n):

     # 找到最近邻
     nearestk=[]
     distances = computeNearestNeighbor(username, test,train)
     for i in range(k):
         nearestk.append(distances[i])
     recommendations = []
     predict={}
     # 找到最近邻看过，但是user没看过的电影，计算推荐
     for nearest in nearestk:
        neighborRatings = train[nearest[1]]
        userRatings = train[username]
        for artist in neighborRatings:
           if not artist in userRatings:
               if artist in predict:
                   predict[artist]=predict[artist]+neighborRatings[artist]*nearest[0]
               else:
                    predict[artist]=neighborRatings[artist]*nearest[0]
     for movie in predict:
         x=0
         for nearest in nearestk:
               neighborRatings = train[nearest[1]]
               if movie in neighborRatings:
                 x=x+nearest[0]
         predict[movie]=predict[movie]/x
     sse = 0
     #print(predict)
     if username in test:
      for movie in test[username]:
         if movie in predict:
             sse = sse + abs(test[username][movie] - predict[movie])**2
         else :
             sse=sse+5/k
     predict = sorted(predict.items(), key=lambda x: x[1], reverse=True)
     l=[]
     for i in range(n):
         l.append(predict[i][0])
     print(username+'推荐为:')
     print(l)
     return(sse)

if __name__ == '__main__':
    test = {}
    train = {}
    jug = {}
    file1 = open('test_set.csv')
    file2 = open('train_set.csv')
    file3 = open('ratings.csv')
    ReadData(file1, test)
    ReadData(file2, train)
    ReadData(file3, jug)
    #for user in test:
    sse=0
    for user in test:
       sse=sse+recommend(user, test, train, 20, jug, 10)
    print(sse)
    recommend('5', test, train, 20, jug, 10)