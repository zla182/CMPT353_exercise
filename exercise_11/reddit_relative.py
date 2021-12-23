'''
Author: your name
Date: 2021-11-24 12:56:27
LastEditTime: 2021-11-26 17:01:49
LastEditors: Please set LastEditors
Description: 
FilePath: \e11\reddit_relative.py
'''
import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)

    # TODO
    comments = comments.cache()
    groups = comments.groupBy('subreddit')
    averages = groups.agg(functions.avg(comments['score']).alias("average_score"))
    averages= averages.filter(averages.average_score >0)
    averages = averages.cache()
    averages = comments.join(functions.broadcast(averages), 'subreddit')
    averages = averages.withColumn('relative_score', averages['score']/averages['average_score'])
    averages = averages.groupBy('subreddit').agg(functions.max(averages.relative_score).alias("rel_score"))
    
    best_author = groups.agg(functions.max(comments['score']).alias("score"))
    best_author = best_author.cache()
    best_author = comments.join(functions.broadcast(best_author), ['score','subreddit'])
    best_author = best_author.join(averages, 'subreddit')
    best_author = best_author.select('subreddit', 'author', 'rel_score')
    best_author.write.json(out_directory, mode='overwrite')
    
if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
