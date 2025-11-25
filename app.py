# Import all functions from the services module
from servicios import *



def main():
    # In-memory database where the book information will be stored.
    bd = [
        {'title': 'amor',
        'author': 'antonio', 
        'types': 'romance', 
        'precio': 12000.0, 
        'many': 2},
        {'title': 'muerte',
        'author': 'juan', 
        'types': 'terror', 
        'precio': 20000.0, 
        'many': 4
        },
        {'title': 'lucha',
        'author': 'pepe', 
        'types': 'accion', 
        'precio': 12300.0, 
        'many': 6
        },
        {'title': 'fantacia',
        'author': 'luisa', 
        'types': 'anime', 
        'precio': 3405.0, 
        'many': 3
        },
        {'title': 'que',
        'author': 'el tio', 
        'types': 'cualquiera', 
        'precio': 12323.0, 
        'many': 4
        }
        ]
    # In-memory database where sales records will be stored.
    bd_assign = []

    # Main application loop to display the menu.
    while True:
        print("\nWelcome to the National Library")
        print("\n===== MENU LIBRERÍA NACIONAL =====")
        print("1. Ingresar libro.")
        print("2. Mostrar libros.")
        print("3. Buscar libro.")
        print("4. Actualizar libro")
        print("5. Eliminar libro.")
        print("6. Registrar libro vendido.")
        print("7. Mostrar libros vendidos")
        print("8. Módulo de reportes")        
        
        

        option = input("Ingrese una opcion: ")
        
        # Validate that the input is a number.
        if not option.isdecimal():
            print("Opcion invalida")
            continue

        option = int(option)

        # Option 1: Add a new book
        if option == 1:
            title = input("Titulo del libro: ")
            # Validate that the title is not empty
            if not title:
                print("El titulo no puede estar vacío.")
                continue
            # Get book details from user
            author = str(input("Nombre del autor del libro: "))
            if not author:
                print("El nombre del autor no puede estar vacío.")
                continue
            types = input("Categoria del libro: ")
            if not types:
                print("La fecha no puede estar vacía.")
                continue
            # Handle potential errors with numeric inputs
            try:
                precio = float(input("Precio del libro: "))
                many = int(input("Cantidad de libros: "))
                if not precio or not many:
                    print("La cantidad y el precio no pueden estar vacios")
                    continue
                if many < 0 or precio < 0:
                    print("La cantidad y el precio no puede ser negativa.")
                    continue

            except ValueError:
                print("La cantidad debe ser numerico.")
                continue

            add_book(bd,title,author,types,precio,many)
# Option 2: Display all books
        elif option == 2:
            list_books(bd)
# Option 3: Search for a book
        elif option == 3:
            nom = input("Titulo del libro a buscar: ")
            if not nom:
                print("El Titulo no puede estar vacía.")
                continue
            book = search_books(bd,nom)
            if book:
                print(book)
            else:
                print("No se encontro el libro.")

        # Option 4: Update a book
        elif option == 4:
            nom = input("Titulo del libro a actualizar: ")
            if not nom:
                print("El Titulo no puede estar vacía.")
                continue
            try:
                # Get new data, allowing empty inputs to keep old values
                author = input("Nuevo autor del libro (ENTER PARA NO CAMBIAR): ")
                author = str(author) if author else None

                types = input("Nueva categoria del libro (ENTER PARA NO CAMBIAR NADA): ")
                types = (types) if types else None

                precio = input("Nuevo Precio (ENTER PARA NO CAMBIAR NADA): ")
                precio = float(precio) if precio else None

                many = input("Nueva cantidad de libros (ENTER PARA NO CAMBIAR): ")
                many = int(many) if many else None

                # Validate new numeric values
                if precio is not None and precio < 0:
                    print("El precio no puede ser negativo.")
                    continue

                if many is not None and many < 0:
                    print("La cantidad no puede ser negativa.")
                    continue

            except ValueError:
                print("El precio y la cantidad deben ser numericos.")
                continue

            update_book(bd,nom,author,types,precio,many)

        # Option 5: Delete a book
        elif option == 5:
            nom = input("Tutulo del libro a eliminar: ")
            if not nom:
                print("El Titulo no puede estar vacío.")
                continue
            delete_book(bd,nom)

        # Option 6: Register a book sale
        elif option == 6:
            nom = input("Titulo del libro a vender: ")
            if not nom:
                print("El Titulo no puede estar vacío.")
                continue
            # Check if the book exists before asking for more details
            book_to_sell = search_books(bd, nom)
            if not book_to_sell:
                print("Error: el libro no existe.")
                continue

            try:
                cus = input("Nombre del cliente: ")
                if not cus:
                    print("El nombre del cliente no puede estar vacío.")
                    continue
                amoun = int(input("Cantidad a vender: "))
                date = input("Fecha de la venta realizada: ")
                if not date:
                    print("La fecha no puede estar vacía.")
                    continue
                # Handle discount input, defaulting to 0.0 if empty
                discount_input = input("Si tiene descuento ingrese cuanto (ENTER SI NO TIENE DESCUENTO): ")
                dis = float(discount_input) if discount_input else 0.0
                
                if amoun <= 0 or dis < 0:
                    print("La cantidad debe ser positiva y el descuento no puede ser negativo.")
                    continue
            except ValueError:
                print("La cantidad y el descuento deben ser numericos.")
                continue

            assign_books(bd, bd_assign, nom, cus, amoun, date, dis)

        # Option 7: Display sold books
        elif option == 7:
            list_assign_books(bd_assign)

        # Option 8: Reports module
        elif option == 8:
            show_reports(bd, bd_assign)




# Entry point of the script
if __name__ == "__main__":
    main()
