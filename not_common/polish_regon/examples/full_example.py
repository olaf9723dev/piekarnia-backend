from not_common.polish_regon.service import RegonService


regon_service = RegonService(sandbox=True)
print(regon_service.search(nip='9111188796'))
