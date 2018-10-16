# Knowledge Graphs 2018: Example data & source code

## Example data format
Example graphs are provided in the following format:

```
n
s_1 t_1
s_2 t_2
…
s_m t_m
```

The first line contains the number of vertices, `n`', as a natural
number.  Each of the following lines specifies a directed edge in the
form `s_i t_i`, where `s_i` is the source vertex and `t_i` is the
target vertex. Vertices are numbered `0, 1, …, n - 1`.
