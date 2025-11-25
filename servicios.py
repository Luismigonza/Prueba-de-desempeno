
#traduce al ingles todos los comentarios y agrega comentarios que creas que faltan en ingles sin dañar el codigo SOLO A LOS COMENTARIOS NO TOQUES EL CODIGO

def add_book(bd,title,author,types,precio,many):
    """
    Adds a new book to the database list.
    """
    
    books = {
        "title": title,
        "author": str(author),
        "types": str(types),
        "precio": float(precio),
        "many": int(many)
    }
    bd.append(books)
    print("Productos agregados correctamente.")

def list_books(bd):
    """
    Displays the list of existing books in a readable format.
    """
    # Check if the database is empty before trying to print.
    if not bd:
        print("No hay Libros registrados.")
        return

    print("\n=== LISTA DE PRODUCTOS ===")
    for book in bd:
        print(f"Libro: {book["title"]} | Autor: {book["author"]} | Categoria: {book["types"]} | Precio: {book["precio"]} | Cantidad: {book["many"]}")

def search_books(bd,nom):
    """
    Searches for a book by its title.
    Returns the book dictionary if found, otherwise returns None.
    """
    for book in bd:
        if book["title"] == nom:
            return book
    # Return None if the loop finishes without finding the book.
    return None

def update_book(bd, name, new_author=None, new_types=None, new_precio=None, new_many=None):
    """
    Updates the data of a specific book if it exists.
    Only the provided fields (not None) will be updated.
    """
    # Find the book to update.
    book = search_books(bd,name)
    if not book:
        print("No se encontro el libro.")
        return
    
    # Update each field only if a new value was provided.
    if new_author is not None:
        book["author"] = new_author
    if new_types is not None:
        book["types"] = new_types
    if new_precio is not None:
        book["precio"] = new_precio
    if new_many is not None:
        book["many"] = new_many

    print("Libro actualizado correctamente.")

def delete_book(bd,name):
    """
    Deletes a book from the database by its title.
    """
    book = search_books(bd,name)
    if book:
        bd.remove(book)
        print("Libro eliminado.")
    else:
        print("No se encontro el producto.")

def assign_books(bd, bd_assign, name, custum, amount, date, discount):
    """
    Registers the sale of a book, associating customer, quantity, date, and discount.
    It also validates and automatically updates the available stock.
    """
    # 1. Find the book to get its details and current stock.
    book = search_books(bd, name)
    # This is a safety check, although app.py already verifies it.
    if not book:
        print(f"Error interno: El libro '{name}' no fue encontrado para la venta.")
        return

    # 2. Validate available stock.
    if book['many'] < amount:
        print(f"Error: No hay suficiente stock para '{name}'. Disponible: {book['many']}, Solicitado: {amount}")
        return

    # 3. Automatically update the stock.
    book['many'] -= amount

    # 4. Register the sale in the sales database.
    total_price = (book['precio'] * amount)
    final_price = total_price - discount if discount is not None else total_price

    sale_record = {'title': name, 'customer': custum, 'amount': amount, 'date': date, 'discount': discount, 'final_price': final_price}
    bd_assign.append(sale_record)
    print(f"Venta registrada exitosamente. Stock actualizado para '{name}': {book['many']} unidades restantes.")

def list_assign_books(bd_assign):
    """
    Displays the list of sold books (sales records) in a readable format.
    """
    if not bd_assign:
        print("No hay Libros registrados.")
        return

    print("\n=== LISTA DE PRODUCTOS ===")
    for book in bd_assign:
        print(f"Libro: {book["title"]} | Cliente: {book["customer"]} | Cantidad: {book["amount"]} | Fecha de la venta: {book["date"]} | Precio final: ${book["final_price"]}")

def calculate_report_data(bd, bd_assign):
    """
    Calculates all the necessary data for the reports from the sales records.
    Returns a dictionary with the processed data, or None if there are no sales.
    """
    if not bd_assign:
        return None
    

    # 1. Calculate total units sold per book title.
    sold_count = {}
    for sale in bd_assign:
        title = sale['title']
        amount = sale['amount']
        sold_count[title] = sold_count.get(title, 0) + amount

    # 2. Calculate total sales (net income) grouped by author.
    sales_by_author = {}
    for sale in bd_assign:
        book = search_books(bd, sale['title'])
        if book:
            author = book['author']
            sales_by_author[author] = sales_by_author.get(author, 0) + sale['final_price']

    # 3. Calculate total net and gross income.
    net_income = sum(sale['final_price'] for sale in bd_assign)
    total_discounts = sum(sale.get('discount', 0.0) for sale in bd_assign)
    gross_income = net_income + total_discounts

    # 4. Create a ranking of best-selling books (from most to least sold).
    ranking_sold_books = sorted(sold_count.items(), key=lambda item: item[1], reverse=True)

    return {
        "sold_count": sold_count,
        "sales_by_author": sales_by_author,
        "net_income": net_income,
        "gross_income": gross_income,
        "ranking_sold_books": ranking_sold_books
    }

def show_reports(bd, bd_assign):
    """
    Displays the calculations performed in "calculate_report_data"
    in a user-friendly format.
    """
    # Get the calculated data.
    show = calculate_report_data(bd,bd_assign)
    if not show:
        return

    print("\n=== REPORTE DE VENTAS ===")
    print(f"Venta total de libros: ${show['sold_count']}")
    print(f"Libros vendidos por autor: {show['sales_by_author']}")
    print(f"Ingreso neto: ${show['net_income']} | Ingresos brutos: ${show['gross_income']}")
    print(f"\nRankin de libros mas vendidos: ")
    for book, val in show["ranking_sold_books"]:
        print(f"- {book}: ${val:.2f}")
