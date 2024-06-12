
from sqlalchemy import create_engine, text, MetaData, Table, insert
from sqlalchemy import MetaData
import pandas as pd

engine = create_engine("mysql+pymysql://root:example@db/diabetes?charset=utf8mb4")
metadata_obj = MetaData()

df = pd.read_csv("../data/diabetes.csv")
df.head()

test_table = Table("bloodtest_results", metadata_obj, autoload_with=engine)
patient_table = Table("patient", metadata_obj, autoload_with=engine)
diagnosis_table = Table("diagnosis", metadata_obj, autoload_with=engine)

POSITIVE_ID = 1
NEGATIVE_ID = 2

with engine.connect() as conn:
    for i, row in df.iterrows():
        if row["Outcome"] == 1:
            did = POSITIVE_ID
        else:
            did = NEGATIVE_ID
        stmt = (
            insert(test_table).values(
                Pregnancies=row["Pregnancies"], Glucose=row["Glucose"], BloodPressure=row["BloodPressure"], SkinThickness=row["SkinThickness"], 
                Insulin=row["Insulin"], BMI=row["BMI"], DiabetesPedigreeFunction=row["DiabetesPedigreeFunction"], diagnosis_id = did
            )
        )
        result = conn.execute(stmt)
        pid = result.inserted_primary_key[0]

        stmt = (
            insert(patient_table).values(
                first_name = "",
                last_name = "",
                age = row["Age"],
                test_result_id = pid
            )
        )
        conn.execute(stmt)
    conn.commit()
