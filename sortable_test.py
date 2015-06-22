'''
       Michael Bearden
       Sunday June 21 2015
       Sortable coding chalange
       files products.txt and listings.txt should be placed in same directory
       as this file, sortable_test.py.  Results will be printed to file in the 
       same directory in  results.txt
'''


class Product:
    # Basic class for the Product object
    def __init__(self, product_name, manufacturer, family, model, announced_date):
        self.product_name = product_name
        self.manufacturer = manufacturer
        self.family = family
        self.model = model
        self.announced_date = announced_date
        
class Listing:
    # Basic class for the Listing object
    def __init__(self, title, manufacturer, currency, price):
        self.title = title
        self.manufacturer = manufacturer
        self.currency = currency
        self.price = price

class Result:
    #Basic class for the result class
    def __init__(self, product_name, listings):
        self.product_name = product_name
        self.listings = listings
        
def Read_Products_File(products_file):
    '''
        Assuming product_file is a list of products in following formats
        {"product_name":"Konica_Minolta_DiMAGE_EX_1500_Wide","manufacturer":"Konica Minolta","model":"EX 1500 Wide","family":"DiMAGE","announced-date":"1998-08-30T20:00:00.000-04:00"} 
        or
        {"product_name":"Konica_Minolta_DiMAGE_EX_1500_Wide","manufacturer":"Konica Minolta","model":"EX 1500 Wide","announced-date":"1998-08-30T20:00:00.000-04:00"}
        
        extracts strings
        product_name = "Konica_Minolta_DiMAGE_EX_1500_Wide"
        manufacturer = "Konica Minolta"
        model = "EX 1500 Wide"
        family = "DiMAGE"        //  or family = ""
        announced-date = "1998-08-30T20:00:00.000-04:00"
        
        creates a product object with these strings for each line in the file, and 
        returns a list of all products from the file
    '''
    products = []
    for line in products_file:
        temp_string = line.split(",\"announced-date\":\"")
        announced_date = temp_string[1][:-3]
        if "\"family\":" in temp_string[0]:
            temp_string = temp_string[0].split(",\"family\":\"")
            family = temp_string[1][:-1]
        else:
            family = ""
        temp_string = temp_string[0].split(",\"model\":\"")
        model = temp_string[1][:-1]
        temp_string = temp_string[0].split(",\"manufacturer\":\"")
        manufacturer = temp_string[1][:-1]
        product_name = temp_string[0][17:-1]
        
        product = Product(product_name, manufacturer, family, model, announced_date)
        products.append(product)
        
    return products

def Read_Listings_File(listings_file):
    '''
        Assuming listings_file is a list of listings in following formats
        {"title":"LED Flash Macro Ring Light (48 X LED) with 6 Adapter Rings for For Canon/Sony/Nikon/Sigma Lenses","manufacturer":"Neewer Electronics Accessories","currency":"CAD","price":"35.99"}
        
        extracts strings
        title = "LED Flash Macro Ring Light (48 X LED) with 6 Adapter Rings for For Canon/Sony/Nikon/Sigma Lenses"
        manufacturer = "Neewer Electronics Accessories"
        currency = "CAD"
        price = "35.99"
        
        creates a listing object with these strings for each line in the file, and 
        returns a list of all listings from the file
    '''
    listings = []
    for line in listings_file:
        temp_string = line.split(",\"price\":\"")
        price = temp_string[1][:-3]
        temp_string = temp_string[0].split(",\"currency\":\"")
        currency = temp_string[1][:-1]
        temp_string = temp_string[0].split(",\"manufacturer\":\"")
        manufacturer = temp_string[1][:-1]
        title = temp_string[0][10:-1]
        
        listing = Listing(title, manufacturer, currency, price)
        listings.append(listing)
        
    return listings

def Find_Listings(product, Listings):
    '''
        Given a product object, and the list of listings
        return a list containing all the listings of the given product
        current algo is a basic exact string match, first check if manufactuers are same, if its not then its not the correct listing
        secondly check if the product name, model, or family is in the title of the listing
        This should give a high return rate of listings without returning false positives
        to avoid issies with inconsistant case sensitivity, when checking everything goes to upper case.
        A possibly better algo, could be a more complex aproximate string matching, this can return a ,much higher count of listings
        becasue of possible typos and inconsistency within different listings of a product, however this would also return a few more 
        false positives as a slightly different model# could be considered a an inconsistency and be returned
    '''
    listings = []
    for listing in Listings:
        if listing.manufacturer.upper() == product.manufacturer.upper():
            if product.product_name.upper() in listing.title.upper() or product.model.upper() in listing.title.upper() or (product.family != "" and product.family.upper() in listing.title.upper()):
                listings.append(listing)
    return listings

def Create_Results(Products, Listings):
    '''
        For each product finds all listings accroding to Find_Listings algo and create a result object
        return a list of all result objects
    '''
    Results = []
    for product in Products:
        listings = Find_Listings(product, Listings)
        result = Result(product.product_name, listings)
        Results.append(result)
    
    return Results

def Print_Results(Results, results_file):
    '''
        Prints the list of results to the result file in JSON format
        example
        {"product_name":"Epson_C900Z","listings":[]}
        {"product_name":"Olympus-SP610UZ","listings":[{"title":"Olympus - SP-610 UZ - Appareil Photo Bridge - 14 Mpix - Zoom 22x - Noir","manufacturer":"Olympus","currency":"EUR","price":"163.24"},{"title":"Olympus - SP-610 UZ - Appareil Photo Bridge - 14 Mpix - Zoom 22x - Noir","manufacturer":"Olympus","currency":"EUR","price":"199.00"}]}
    '''
    for result in Results:
        line = "{\"product_name\":\"" + result.product_name + "\",\"listings\":["
        for listing in result.listings:
            line = line + "{\"title\":\"" + listing.title + "\",\"manufacturer\":\"" + listing.manufacturer + "\",\"currency\":\"" + listing.currency + "\",\"price\":\"" + listing.price + "\"},"
        if len(result.listings) > 0:
            line = line[:-1] # removes extra comma from the list of listings
        line = line + "]}\n"
        
        results_file.write(line)

if __name__=='__main__':
    products_file = open("products.txt" , 'r', encoding="utf8")
    listings_file = open("listings.txt" , 'r', encoding="utf8")
    results_file = open("results.txt", 'w', encoding="utf8")
    
    Products = Read_Products_File(products_file)
    Listings = Read_Listings_File(listings_file)
    
    Results = Create_Results(Products, Listings)
    Print_Results(Results, results_file)
    
    products_file.close()
    listings_file.close()
    results_file.close()