from factordb.factordb import FactorDB
import math

N = 510143758735509025530880200653196460532653147

f = FactorDB(N)

f.get_factor_list()

f.connect()

print(f.get_factor_list())

p, q = f.get_factor_list()


print(min(p, q))