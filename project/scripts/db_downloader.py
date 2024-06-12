from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy import MetaData
import pandas as pd

engine = create_engine("mysql+pymysql://root:example@db/diabetes?charset=utf8mb4")
metadata_obj = MetaData()


test_table = Table("bloodtest_results", metadata_obj, autoload_with=engine)
patient_table = Table("patient", metadata_obj, autoload_with=engine)
diagnosis_table = Table("diagnosis", metadata_obj, autoload_with=engine)


framer = []
with engine.connect() as conn:
    stmt = (
        select(test_table.c[1:], patient_table.c.age, diagnosis_table.c[1:])
        .select_from(test_table)
        .join(patient_table, test_table.c.id == patient_table.c.test_result_id)
        .join(diagnosis_table, test_table.c.diagnosis_id == diagnosis_table.c.id)
    )
    result = conn.execute(stmt)
    for row in result:
        framer.append(row._asdict())


df = pd.DataFrame(framer)
df.Outcome = df.Outcome.apply(lambda x: {"Positive": 1, "Negative": 0}[x])
df.to_csv("../data/diabetes.bak.csv", index=False)
