MATCH (p:Person)-[r]->(m:Movie)
WITH p, m, collect(TYPE(r)) AS rs
WHERE SIZE(rs) > 1
RETURN p.name, m.title, rs