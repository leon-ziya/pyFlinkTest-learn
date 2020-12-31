#-*-coding:utf-8-*-
import shutil
from pyflink.table import TableConfig, DataTypes, BatchTableEnvironment, EnvironmentSettings
import os


# 创建执行环境---Blink批处理环境
env_settings = EnvironmentSettings.new_instance().in_batch_mode().use_blink_planner().build()
t_env = BatchTableEnvironment.create(environment_settings=env_settings)

# 创建执行环境---Flink处理环境
# env_settings = EnvironmentSettings.new_instance().in_batch_mode().use_old_planner().build()
# t_env = BatchTableEnvironment.create(environment_settings=env_settings)

# 数据源文件
# source指定数据源，即待处理的数据流的源头，这里使用同级目录下的source.csv，实际中可能来自于mysql、kafka、Hive
#dir_source = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'source.csv')
dir_source = "jianglai/test/source.csv"

# 计算结果文件
# sink 指发送数据，即带处理的数据流的出口，这里使用同级目录下的sink.csv，实际中可能会把处理好的数据存储到mysql、kafka、Hive等
#dir_sink = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sink.csv')
dir_sink = "jianglai/test/myDemo/wordcount"

# 如果结果文件已经存在，就删除
if os.path.exists(dir_sink):
    if os.path.isfile(dir_sink):
        os.remove(dir_sink)
    else:
        shutil.rmtree(dir_sink, True)


# 创建数据源表
# TODO 基于SQL API
t_env.execute_sql(f"""
    CREATE TABLE source(
        id BIGINT,
        word STRING
    ) WITH(
        'connector'='filesystem',
        'path' = 'hdfs://mycluster/{dir_source}',
        'format' = 'csv'
    )
    """
)

# 创建结果表
# TODO 基于 SQL API
t_env.execute_sql(f"""
    CREATE TABLE sink(
        word STRING,
        cnt BIGINT
    ) WITH(
        'connector' = 'filesystem',
        'path' = 'hdfs://mycluster/{dir_sink}',
        'format' = 'csv'
    )
    """
)

# 非常简单的wordcount计算逻辑
# TODO  基于 SQL API
t_env.execute_sql(f"""
    INSERT INTO sink
    SELECT word,
           count(1) AS cnt
    FROM source
    GROUP BY word
""")

# t_env.from_path('source').print_schema()
# print(t_env.from_path('source').to_pandas())
#
#t_env.from_path('sink').print_schema()
print(t_env.from_path('sink').to_pandas())
