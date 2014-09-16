__author__ = 'Daniil'
import json
cur = {}
lit = open('t.txt', 'rb').readlines()
for ga in lit:
    ga = ga.replace('\r\n', '')
    html = "%sPage/%sPage.html" % (ga.split("ga:")[1], ga.split("ga:")[1])
    tmp = {ga: {"view": "Metrics", "html": html, "value": False}}
    cur.update(tmp)
print cur

# "Dimensions"
# "Metrics"