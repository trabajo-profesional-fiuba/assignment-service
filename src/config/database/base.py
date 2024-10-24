from sqlalchemy.orm import declarative_base

# Esta clase Base es una instancia de una declarative_base
# La cual es necesaria para que el resto de las clases tengan que ser 
# Hereadadas de esta

Base = declarative_base()
