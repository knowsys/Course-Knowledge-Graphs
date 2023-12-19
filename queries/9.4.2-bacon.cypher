MATCH (b:Person {name:"Kevin Bacon"})
MATCH p = shortestPath( (other:Person)-[*]-(b) )
WHERE other <> b
RETURN other.name, LENGTH(p)