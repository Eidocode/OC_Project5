
from category import Category
from product import Product
from colorama import init, deinit, Fore, Back, Style


init(autoreset=True)


menu_is_active = True

while menu_is_active :
    print("1 : Afficher l'état de la base")
    print("2 : Ajouter des catégories")
    print("3 : Ajouter des produits")
    print("")
    print("0 : EXIT")

    user_input = input("Que souhaitez-vous faire : ")

    if user_input == '0':
        print("exiting....")
        menu_is_active = False
    elif user_input == '1':
        category = Category()
        product = Product()
        nb_catg = len(category.categories_in_db)
        nb_prod = len(product.products_in_db)
        print("La base contient actuellement : {} catégories | {} produits.".format(nb_catg, nb_prod))
        category._destroy()
        product._destroy()
    elif user_input == '2':
        category = Category()
        nb = input("Combien de catégories souhaitez-vous ajouter : ")
        category.set_to_db(category._get_from_api(int(nb)))
        category._destroy()
    elif user_input == '3':
        product = Product()
        nb = input("Combien de produits/catégorie souhaitez-vous ajouter : ")
        product.set_to_db(product._get_from_api(int(nb)))
        product._destroy

deinit()
