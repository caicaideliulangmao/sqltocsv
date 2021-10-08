# sqltocsv
读数据库表写入CSV
目前实现mssql和oracle

mssqltocsv可以直接使用pyinstaller进行编译
使用方法：
msql2csv.exe <server> <database> <username> <password> <tablename> <filepath>
filepath为CSV存储文件地址
导入CSV文件会以十万条数据生成一个CSV，一百万数据则有十个CSV
  
oracletocsv需要两步编译
pyinstaller -F -w orac2csv.py
pyinstaller orac2csv.spec
编译的orac2csv.spec需要按照spec文件下的文件orac2csv.spec进行修改
ora2csv.exe <server> <database> <username> <password> <tablename> <filepath>
filepath为CSV存储文件地址
导入CSV文件会以十万条数据生成一个CSV，一百万数据则有十个CSV
打包需要注意oracle版本问题，若提示版本不支持，改动dll文件，重新编译即可
