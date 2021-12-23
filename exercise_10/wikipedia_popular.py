'''
Author: your name
Date: 2021-11-17 12:54:57
LastEditTime: 2021-11-17 15:52:43
LastEditors: Please set LastEditors
Description: 
FilePath: \exercise_10\wikipedia_popular.py
'''
import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wiki_schema = types.StructType([
    types.StructField('lang', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('views', types.LongType()),
    types.StructField('bytes', types.LongType()),
])

# https://docs.python.org/3/library/re.html
def file2date(pathname):
    result = re.search("([0-9]{8}\-[0-9]{2})", pathname)
    return result.group(1)

def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, schema=wiki_schema, sep=' ').withColumn('filename', functions.input_file_name())
    
    cleaned_data = data.filter(data['lang'] == 'en')
    cleaned_data = cleaned_data.filter(data['title'] != 'Main_Page')
    cleaned_data = cleaned_data.filter(data.title.startswith('Special:') == False)
    path_to_hour = functions.udf(lambda path: file2date(path), returnType=types.StringType())
    cleaned_data = cleaned_data.withColumn('date', path_to_hour(cleaned_data.filename))
    cleaned_data = cleaned_data.drop('language', 'bytes', 'filename')
    cleaned_data = cleaned_data.cache()
    groups = cleaned_data.groupBy('date')
    most_viewed = groups.agg(functions.max(cleaned_data['views']).alias('views')) #most views by date   
    data_joined = most_viewed.join(cleaned_data, on=['views','date'])
    output = data_joined.drop('lang', 'bytes', 'filename')
    output = output.select('date', 'title', 'views')
    output = output.sort('date','title')
    #output.show()

    output.write.csv(out_directory + '-wikipedia', mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)