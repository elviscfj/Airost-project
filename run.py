from web.web import Web

test = Web()

with Web() as test:
    test.main()
    test.scrap()
 
    