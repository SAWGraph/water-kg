import requests
requests.packages.urllib3.disable_warnings()

#get equivalent facility id from frs
pwsid = 'ME0000002'

facility_json = requests.get(url=f'https://frs-public.epa.gov/ords/frs_public2/frs_rest_services.get_facilities?pgm_sys_acrnm=SFDW&pgm_sys_id={pwsid}&program_output=yes&output=JSON')
print(facility_json)