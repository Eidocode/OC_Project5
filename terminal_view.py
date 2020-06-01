from colorama import init, deinit, Fore, Back, Style

from controler import Controler


init(autoreset=True)

controler = Controler()

def menu1():
    print("--")
    print("1 : Afficher l'état de la base")
    print("2 : Consulter la liste des catégories")
    print("3 : Sélectionner une catégorie")
    print("4 : Ajouter de nouvelles catégories")
    print("5 : Ajouter de nouveaux produits dans toutes les catégories existantes")
    print("--")
    print("0 : EXIT")
    print("--")

def menu2():
    print("--")
    print("1 : Afficher tous les produits")
    print("2 : Ajouter des produits")
    print("3 : Consulter un produit")
    print("--")
    print("0 : Return")
    print("--")

def show_product_information(product):
    if product != None:
        print("*****************************")
        print("Vous avez sélectionné le produit " + product['name'] + " de la marque " + str(product['brand']))
        print("-----")
        print("-----")
        print("Nutriscore : " + str(product['nutriscore']).upper())
        print("-----")
        print("Dans quelle(s) ville(s) peut-on le trouver : " + str(product['places']))
        print("-----")
        print("Dans quel(s) magasin(s) peut-on l'acheter : " + str(product['stores']))
        print("-----")
        print("Code barre : " + str(product['barcode']))
        print("-----")
        print("Description : " + str(product['description']))
        print("*****************************")
    else:
        print("*****************************")
        print("Ce produit n'existe pas ou appartient a une autre catégorie... Veuillez saisir un ID existant dans cette catégorie...")
        print("*****************************")

def show_category_information(category):
    if category != None:
        print("*****")
        print ("vous avez sélectionné la catégorie " + str(category['id']) + " : " + category['name'])
        print("*****")
    else:
        print("*****************************")
        print("Cette catégorie n'existe pas... Veuillez saisir un ID existant...")
        print("*****************************")
        return False
    return True


menu1_is_active = True
menu2_is_active = False

while menu1_is_active :
    menu1()
    user_input = input("Quel action souhaitez vous effectuer : ")

    if user_input == '0':
        print("Exiting....")
        menu1_is_active = False
    elif user_input == '1':
        db_status = controler.get_database_status()
        print("*****")
        print(db_status)
        print("*****")
    elif user_input == '2':
        print("*****")
        controler.get_all_categories_info()
        print("*****")
    elif user_input == '3':
        id_cat = input("Veuillez saisir l'ID de la catégorie : ")
        selected_category = controler.get_category_info(id_cat)
        if show_category_information(selected_category):
            menu2_is_active = True

        while (menu2_is_active):
            menu2()
            user_new_input = input("Quel action souhaitez vous effectuer sur la catégorie : ")

            if user_new_input == '0':
                menu2_is_active = False
            elif user_new_input == '1':
                controler.get_all_products_info(id_cat)
            elif user_new_input == '2':
                input_prod = input("Combien de produits souhaitez-vous ajouter dans cette catégorie : ")
                controler.set_products_in_category(input_prod, id_cat)
            elif user_new_input == '3':
                input_prod = input("Quel produit souhaitez-vous consulter : ")
                this_product = controler.get_product_info(input_prod, id_cat)
                show_product_information(this_product)
            else:
                print("Ce choix n'existe pas... Veuillez recommencer...")
        
    elif user_input == '4':
        nb_cat = input("Combien de catégories souhaitez-vous ajouter : ")
        controler.set_categories(nb_cat)
    elif user_input == '5':
        nb_prod = input("Combien de produits par catégorie souhaitez-vous ajouter : ")
        controler.set_products(nb_prod)
    else:
        print("Ce choix n'existe pas... Veuillez recommencer...")
        

deinit()
