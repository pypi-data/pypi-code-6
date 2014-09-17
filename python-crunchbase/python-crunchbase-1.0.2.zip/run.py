from crunchbase import CrunchBase
cb = CrunchBase('00cfa4fabf29d7b5a1cb615b66e709ef')
with open('companies_sm.txt','r') as f:
	lines = f.readlines()
with open('out.csv', 'w') as f:
	for line in lines:
		sm_org = cb.getOrganizations(line)['data']['items']
		if len(sm_org) > 0:
			funding = cb.getOrganization(sm_org[0]['path'])['data']['properties']['total_funding_usd']
			print line
			print sm_org
			print funding
			f.write(line+','+sm_org[0]['name']+','+str(funding)+'\n')
		else:
			f.write(line+',,\n')