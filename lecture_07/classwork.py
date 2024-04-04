import pandas as pd


df_students = pd.read_excel("./lecture_07/students.xlsx", index_col=False)
df_students.drop(columns=["Unnamed: 0"], inplace=True)

df_subjects = pd.read_excel("./lecture_07/subjects.xlsx", index_col=False)


def get_random_subjects():
    classes = []
    credits = 0
    for i in df_subjects.sample(frac=1).iterrows():
        if (credits + i[1]['კრედიტები']) <= 30:
            credits += i[1]['კრედიტები']
            classes.append(i[1]['სასწავლო კომპონენტი'])
        if credits == 20:
            break
    return classes


all_classes = []
for i in df_students.iterrows():
    classes = get_random_subjects()
    all_classes.append(classes)

df_selected_subjects = pd.DataFrame(all_classes, columns=["საგანი 1", "საგანი 2", "საგანი 3", "საგანი 4"])

df_full = pd.concat([df_students, df_selected_subjects], axis=1)
df_full.to_excel("student_subjects.xlsx", index=False)
