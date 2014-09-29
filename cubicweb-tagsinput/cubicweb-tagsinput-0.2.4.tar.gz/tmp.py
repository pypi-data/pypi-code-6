q1, q2 = __args__[:1]

r1 = 'Any P, FTIRANK(P) WHERE P is Place, P has_text %(q1)s'

r2 = '''Any P, AVG(FTIRANK(A)) GROUPBY P
WHERE P is Place, P mailaddress A, A has_text %(q2)s'''

r3 = 'Any P, SUM(R) GROUPBY P WITH P, R BEING ((%s) UNION (%s))' % (r1, r2)


for r in (r1, r2, r3):
    rset = rql(r, {'q': q})
    print rset
