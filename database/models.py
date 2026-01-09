from sqlalchemy import Table,Column,Integer,String,Boolean,MetaData

metadata_obj = MetaData()

table = Table(
    "user_data_table",
    metadata_obj,
    Column("username",String,primary_key=True),
    Column("sub",Boolean)
)

