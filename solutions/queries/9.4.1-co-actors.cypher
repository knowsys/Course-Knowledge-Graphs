MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(b:Person),
      (a)-[:ACTED_IN]->(n:Movie)<-[:ACTED_IN]-(b)
WHERE a.name < b.name AND m.title < n.title
RETURN a.name, b.name