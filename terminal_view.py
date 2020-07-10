from colorama import init, deinit, Fore

from controller import Controller


init(autoreset=True)

controller = Controller()


def main_menu():
    # Terminal main menu
    print("--")
    print("1 : Afficher l'état de la base")
    print("2 : Sélectionner une catégorie")
    print("3 : Consulter les favoris")
    print("4 : Ajouter 5 catégories dans la base")
    print("5 : Ajouter 5 produits dans toutes les catégories existantes")
    print("--")
    print("0 : EXIT")
    print("--")


def catg_menu():
    # Terminal categories menu
    print("--")
    print("1 : Sélectionner un produit")
    print("2 : Ajouter 5 produits dans la catégorie")
    print("--")
    print("0 : Return")
    print("--")


def prod_menu():
    # Terminal products menu
    print("--")
    print("1 : Ajouter ce produit comme favori")
    print("2 : Consulter un produit substitut")
    print("--")
    print("0 : Return")
    print("--")


def fav_menu():
    # Terminal favorites menu
    print("--")
    print("1 : Sélectionner un favori")
    print("--")
    print("0 : Return")
    print("--")


def show_product_information(product):
    # Product sheet which is displayed when the user wants to consult a product
    if product is not None:
        print("*****************************")
        str1 = "Sélection du produit {} de la marque {}".format(
                                    product['name'], str(product['brand']))
        print(str1)
        print("-----")
        print("-----")
        print("Nutriscore : " + str(product['nutriscore']).upper())
        print("-----")
        str2 = """Dans quelle(s) ville(s) peut-on le trouver : {}""".format(
                                    str(product['places']))
        print(str2)
        print("-----")
        str3 = """Dans quel(s) magasin(s) peut-on l'acheter : {}""".format(
                                    str(product['stores']))
        print(str3)
        print("-----")
        print("Code barre : " + str(product['barcode']))
        print("-----")
        print("Description : " + str(product['description']))
        print("*****************************")
    else:
        print("*****************************")
        print("Ce produit n'existe pas ou appartient à une autre catégorie..")
        print("*****************************")


def show_category_information(category):
    if category is not None:
        print("*****")
        str1 = "Vous avez sélectionné la catégorie {} : {} ".format(
                                    str(category['id']), category['name'])
        print(str1)
        print("*****")
    else:
        print("*****************************")
        print("Cette catégorie n'existe pas, veuillez saisir un ID existant")
        print("*****************************")
        return False
    return True


def main_program():
    main_menu_is_active = True
    catg_menu_is_active = False
    prod_menu_is_active = False
    fav_menu_is_active = False

    while main_menu_is_active:
        main_menu()
        user_input = input("Quelle action effectuer : ")

        if user_input == '0':
            print(Fore.RED + "Exiting....")
            main_menu_is_active = False
        elif user_input == '1':
            db_status = controller.get_database_status()
            print("*****")
            print(db_status)
            print("*****")
        elif user_input == '2':
            print("*****")
            controller.get_all_categories_info()
            print("*****")
            print("--")
            id_cat = input("Veuillez saisir l'ID de la catégorie : ")
            selected_category = controller.get_category_info(id_cat)
            if show_category_information(selected_category):
                catg_menu_is_active = True

            while (catg_menu_is_active):
                catg_menu()
                user_catg_input = input("Quelle action effectuer: ")

                if user_catg_input == '0':
                    catg_menu_is_active = False
                elif user_catg_input == '1':
                    lst_prod = None
                    lst_prod = controller.get_all_products_info(id_cat)
                    inp_prd = input("Quel produit souhaitez-vous consulter : ")
                    prod_menu_is_active = True
                    this_product = controller.get_product_info(
                                                inp_prd, id_cat)
                    show_product_information(this_product)

                    while prod_menu_is_active:
                        prod_menu()
                        user_prod_input = input("Quelle action effectuer : ")

                        if user_prod_input == '0':
                            prod_menu_is_active = False
                        elif user_prod_input == '1':
                            controller.set_product_to_fav(this_product)
                        elif user_prod_input == '2':
                            this_sub = controller.get_sub_product(
                                    this_product, lst_prod)
                            print("##### SUBSTITUTE #####")
                            show_product_information(this_sub)

                            question = True
                            while question:
                                str_input = "Ajouter aux favoris (y/N) : "
                                user_sub_input = input(str_input)
                                if str(user_sub_input.lower()) == 'y':
                                    controller.set_product_to_fav(this_sub)
                                    question = False
                                elif user_sub_input.lower() == 'n' or \
                                        user_sub_input == '':
                                    question = False
                                else:
                                    print("Ce choix n'existe pas...")
                        else:
                            print("Ce choix n'existe pas...")

                elif user_catg_input == '2':
                    controller.set_products_in_category(5, id_cat)
                else:
                    print("Ce choix n'existe pas...")

        elif user_input == '3':
            fav_menu_is_active = True

            while fav_menu_is_active:
                fav_menu()
                user_fav_input = input("Quelle action effectuer : ")

                if user_fav_input == '0':
                    fav_menu_is_active = False
                elif user_fav_input == '1':
                    all_fav = controller.get_all_favorites_info()
                    list_id = []
                    for fav in all_fav:
                        list_id.append(fav['prod_id'])
                    input_fav = input("Quel favori souhaitez-vous consulter :")

                    if int(input_fav) in list_id:
                        this_fav = controller.get_product_info(input_fav)
                        show_product_information(this_fav)
                    else:
                        print("Ce produit n'existe pas dans les favoris... ")
                else:
                    print("Ce choix n'existe pas...")

        elif user_input == '4':
            controller.set_categories(5)
        elif user_input == '5':
            controller.set_products(5)
        else:
            print("Ce choix n'existe pas...")


deinit()
