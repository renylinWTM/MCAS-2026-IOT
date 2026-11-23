import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = np.loadtxt("Bank_Customer.csv", skiprows=1, dtype=str, delimiter=',')

'''
Your work
非數值型資料需轉換成數值型資料 (country, gender)
去除掉無意義的特徵類別 (customer_id)
標準化特徵 (StandardScaler)
'''

# 將 country 轉換成數值型資料
data[data[:, 2] == "France", 2] = "0"
data[data[:, 2] == "Germany", 2] = "1"
data[data[:, 2] == "Spain", 2] = "2"

# 將 gender 轉換成數值型資料
data[data[:, 3] == "Female", 3] = "0"
data[data[:, 3] == "Male", 3] = "1"

# 去除無意義的 customer_id 欄位
data = np.delete(data, 0, axis=1)
data = data.astype(float)

# 最後一欄 churn 是分類答案，其餘欄位是模型特徵
x = data[:, :-1]
y = data[:, -1]

# 標準化特徵
scaler = StandardScaler()
x = scaler.fit_transform(x)

# 將標準化後的特徵與 churn 合併
pre_data = np.column_stack((x, y))

np.savetxt("Bank_Customer_Preprocessed.csv", pre_data, delimiter=",")


from sklearn.linear_model import LogisticRegression
# 決策分類器
clf = LogisticRegression()

'''
Your work
切割 data 為 x_train, x_test, y_train, y_test
請學習 train_test_split 的使用方法
'''

# 將資料切割成 80% Training data 與 20% Testing data
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 使用訓練集來訓練我們的分類器
clf.fit(x_train, y_train)
# 測試資料集中進行預測
pred = clf.predict(x_test)

#print (pred) # 預測分類，即客戶是否流失
#print (y_test) # 分類
print (str(accuracy_score(pred, y_test)*100 ) + "% ")   # 預測精度
