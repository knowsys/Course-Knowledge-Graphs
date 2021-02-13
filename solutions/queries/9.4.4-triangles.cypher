MATCH tri = (a)--(b)--(c)--(a)
RETURN COUNT(distinct(tri))