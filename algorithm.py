"""Module providing the assignment algorithm that solves the assignment 
of teams to topics and tutors."""

# pylint: disable=E0401
import networkx as nx

# grupo1 con todos los temas
grupo1_t1 = ("g1", "t1", {"capacity": 1, "weight": 1})
grupo1_t2 = ("g1", "t2", {"capacity": 1, "weight": 2})
grupo1_t3 = ("g1", "t3", {"capacity": 1, "weight": 3})
grupo1_t4 = ("g1", "t4", {"capacity": 1, "weight": 4})
grupo1_t5 = ("g1", "t5", {"capacity": 1, "weight": 4})
grupo1_t6 = ("g1", "t6", {"capacity": 1, "weight": 4})

# grupo2 con todos los temas
grupo2_t1 = ("g2", "t1", {"capacity": 1, "weight": 4})
grupo2_t2 = ("g2", "t2", {"capacity": 1, "weight": 4})
grupo2_t3 = ("g2", "t3", {"capacity": 1, "weight": 4})
grupo2_t4 = ("g2", "t4", {"capacity": 1, "weight": 1})
grupo2_t5 = ("g2", "t5", {"capacity": 1, "weight": 2})
grupo2_t6 = ("g2", "t6", {"capacity": 1, "weight": 3})

# grupo3 con todos los temas
grupo3_t1 = ("g3", "t1", {"capacity": 1, "weight": 1})
grupo3_t2 = ("g3", "t2", {"capacity": 1, "weight": 4})
grupo3_t3 = ("g3", "t3", {"capacity": 1, "weight": 2})
grupo3_t4 = ("g3", "t4", {"capacity": 1, "weight": 4})
grupo3_t5 = ("g3", "t5", {"capacity": 1, "weight": 3})
grupo3_t6 = ("g3", "t6", {"capacity": 1, "weight": 4})

# Creamos las aristas source a grupos
s_grupo1 = ("s", "g1", {"capacity": 1, "weight": 1})
s_grupo2 = ("s", "g2", {"capacity": 1, "weight": 1})
s_grupo3 = ("s", "g3", {"capacity": 1, "weight": 1})

# Temas hacia los profesores
t1_p1 = ("t1", "p1", {"capacity": 3, "weight": 1})
t2_p1 = ("t2", "p1", {"capacity": 3, "weight": 1})
t3_p2 = ("t3", "p2", {"capacity": 3, "weight": 1})
t4_p2 = ("t4", "p2", {"capacity": 3, "weight": 1})
t5_p2 = ("t5", "p2", {"capacity": 3, "weight": 1})
t6_p2 = ("t6", "p2", {"capacity": 3, "weight": 1})

# Creamos las aristas profesores a t
p1_t = ("p1", "t", {"capacity": 3, "weight": 1})
p2_t = ("p2", "t", {"capacity": 2, "weight": 1})

#aristas totales
aristas = [grupo1_t1,grupo1_t2,grupo1_t3,grupo1_t4,grupo1_t5,grupo1_t6,
           grupo2_t1,grupo2_t2,grupo2_t3,grupo2_t4,grupo2_t5,grupo2_t6,
           grupo3_t1,grupo3_t2,grupo3_t3,grupo3_t4,grupo3_t5,grupo3_t6,
           s_grupo1,s_grupo2,s_grupo3,
           t1_p1,t2_p1,t3_p2,t4_p2,t5_p2,t6_p2,
           p1_t,p2_t]


# Creo un grafo dirigido
G = nx.DiGraph()

# Creo aristas y vertices
G.add_edges_from(aristas)

mincostFlow = nx.max_flow_min_cost(G, "s", "t")
print(mincostFlow)

alumnos = []

for clave, valor in mincostFlow.items():
    if clave.startswith("g"):
        for k,v in valor.items():
            if v == 1:
                alumnos.append([clave,k])

temas = []
for clave, valor in mincostFlow.items():
    if clave.startswith("t"):
        for k,v in valor.items():
            if v >= 1:
                temas.append([clave,k])

for alumno in alumnos:
    a = alumno[0]
    for tema in temas:
        if tema[0] == alumno[1]:
            print("El grupo", a , "tiene el tema " , tema[0] , "y su tutor es:", tema[1])
            