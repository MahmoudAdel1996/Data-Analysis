#!/usr/bin/env python3
import psycopg2


db = psycopg2.connect(database='news')
c = db.cursor()


def most_popular_articles():
    query = "select * from toparticles limit 3;"
    c.execute(query)
    data = c.fetchall()
    return data


def most_popular_authors():
    query = """select author, sum(view) as view from popular
    group by author order by view desc;"""
    c.execute(query)
    data = c.fetchall()
    return data


def error():
    query = "select date from error where error > 1 order by error;"
    c.execute(query)
    data = c.fetchall()
    return data


var1 = most_popular_articles()
var2 = most_popular_authors()
var3 = error()
with open('output.txt', 'w') as out:
    increment1 = 1
    increment2 = 1
    out.write("# Most popular articles:\n")
    for x in var1:
        out.write("{} - {} - {} views\n".format(increment1, x[0], x[1]))
        increment1 += 1
    out.write("\n# Most popular Authors:\n")
    for x in var2:
        out.write("{} - {} - {} views\n".format(increment2, x[0], x[1]))
        increment2 += 1
    out.write("\n# day of high error rate:\n")
    for x in var3:
        out.write("- {:%B %d, %Y}\n".format(x[0]))
db.close()
print("done! successfully.")
