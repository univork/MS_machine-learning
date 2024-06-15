import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 1) პირველ სვეტში ჩაწერეთ სტაჟიორის პირადი 5 ნიშნა კოდი, რომელიც შესაძლოა იწყებოდეს 0-ებით, ყველასთვის განსხვავებული.
# (მაგალითად: 00012, 45397, 07634 და ა.შ.). (2 ქულა).

ids = np.random.choice(np.arange(0, 10), size=(70,5), replace=True)

real_ids = []
for d in ids:
    real_ids.append("".join(str(x) for x in d))

# 2) შემდეგ 30 სვეტში დააგენერირეთ HR-ის შეფასება შემთხვევითი მთელი რიცხვი 0, 100 შუალედიდან, სულ 70*30 = 2100 ჩანაწერი,
# რომლის 20% შემთხვევითად დატოვეთ ცარიელი. (2ქულა).

hr_scores = np.random.choice(np.arange(0, 101), size=(70, 30)).astype(float)


c = int((70 * 30) * .2)
mask = np.zeros(70 * 30, dtype = bool)
mask[:c] = True
np.random.shuffle(mask)
mask=mask.reshape(70, 30)
hr_scores[mask] = np.nan

df_hr = pd.concat([
    pd.DataFrame(real_ids, columns=["pid"]),
    pd.DataFrame(hr_scores)
], axis=1)
df_hr.to_excel("intern.xlsx", sheet_name="sheet1")

# 3) პირველ სვეტში გადმოიტანეთ sheet1-ში პირველ სვეტში არსებული ჩანაწერები.
# 
# 4) შემდეგ 30 სვეტში დააგენერირეთ IT-ის შეფასება შემთხვევითი მთელი რიცხვი 0, 100 შუალედიდან, სულ 70*30 = 2100 ჩანაწერი,
# რომლის 25% შემთხვევითად დატოვეთ ცარიელი. (2ქულა).

it_scores = np.random.choice(np.arange(0, 101), size=(70, 30)).astype(float)


c = int((70 * 30) * .25)
mask = np.zeros(70 * 30, dtype = bool)
mask[:c] = True
np.random.shuffle(mask)
mask=mask.reshape(70, 30)
it_scores[mask] = np.nan

df_it = pd.concat([
    df_hr[["pid"]],
    pd.DataFrame(it_scores)
], axis=1)
df_it.to_excel("intern.xlsx", sheet_name="sheet2")

# 5) დაადგინეთ შეიძლება თუ არა გამოყენებული იყოს წრფივი რეგრესიის მოდელი HR-ის მიერ 30 დღის განმავლობაში მიღებულ
# შეფასებებსა და IT სამსახურის მიერ 30 დღის განმავლობაში მიღებულ შეფასებების კავშირის დადგენისა და პროგნოზირებისთვის,
# ააგეთ შესაბამისი მოდელი. (ამოცანაში შეძლება აიღოთ საშუალო შეფასებები, ჯამი ან სხვა რაიმე მახასიათებელი თითოეული
# სტაჟიორისთვის HR-ის და IT სამსახურის შეფასებებიდან, გაითვალისწინეთ HR-ის შეფასება არის დამოუკიდებელი X ცვლადი, ხოლო IT
# სამსახურის შეფასება დამოკიდებული y ცვლადი). (2 ქულა).

for col in df_hr.columns[1:]:
    df_hr[col] = df_hr[col].fillna(df_hr[col].mean())

for col in df_it.columns[1:]:
    df_it[col] = df_it[col].fillna(df_it[col].mean())

df_hr["mean_score"] = df_hr.iloc[:,1:].mean(axis=1)
df_it["mean_score"] = df_hr.iloc[:,1:].mean(axis=1)

X = df_hr.iloc[:,1:-1]
y = df_it["mean_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.22, random_state=1)

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)
mean_absolute_error(y_test, pred)
