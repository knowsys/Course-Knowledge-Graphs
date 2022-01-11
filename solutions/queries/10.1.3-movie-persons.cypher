MATCH (p:Person)-[r1]->(m:Movie)<-[r2]-(p)
WHERE type(r1)<>type(r2)
RETURN p.name, m.title