from MhDatabses import MhDatabases
db=MhDatabases()
result=db.executeQuery("select time from pcr  where name=%s group by time",["农夫山泉"])
print(result)

