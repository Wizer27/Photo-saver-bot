from sqlalchemy import Table,Column,String,MetaData

metadata_obj = MetaData()

files_table = Table(
    "files_table",
    metadata_obj,
    Column("username",String),
    Column("filedata",String),
    Column("filename",String)
)