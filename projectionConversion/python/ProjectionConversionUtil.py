import math
import pandas as pd
import pymysql

# 加上字符集参数，防止乱码
dbconn = pymysql.connect(
    host="localhost",
    database="gisrookie",
    user="root",
    passwd="jianglai",
    port=3306,
    charset='utf8'

)

# sql 语句
sql = "select id, longitude, latitude from vehicle_gps limit 10"

# 利用pandas模块导入mysql查询的数据
a = pd.read_sql(sql, dbconn)


def wgs84toWebMercator(lon, lat):
    x = lon*20037508.342789/180
    y = math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
    y = y * 20037508.34789/180
    return x, y


# WebMercator-wgs84


def webMercator2wgs84(x, y):
    lon = x/20037508.34*180
    lat = y/20037508.34*180
    lat = 180/math.pi*(2*math.atan(math.exp(lat*math.pi/180))-math.pi/2)
    return lon, lat


if __name__ == "__main__":
    print(a)
