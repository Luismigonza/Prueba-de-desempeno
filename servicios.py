

def add_book(bd,title,author,types,precio,many):
    """
    Agrega los libros a la base de datos.
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
    mostrar la lista de libros existentes en formato legible.
    """
    
    if not bd:
        print("No hay Libros registrados.")
        return

    print("\n=== LISTA DE PRODUCTOS ===")
    for book in bd:
        print(f"Libro: {book["title"]} | Autor: {book["author"]} | Categoria: {book["types"]} | Precio: {book["precio"]} | Cantidad: {book["many"]}")

def search_books(bd,nom):
    """
    Buscar un libro por nombre. Retorna el diccionario o None
    """
    for book in bd:
        if book["title"] == nom:
            return book
    return None

def update_book(bd, name, new_author=None, new_types=None, new_precio=None, new_many=None):
    """
    Actualizar datos de un libro si existe.
    """
    book = search_books(bd,name)
    if not book:
        print("No se encontro el libro.")
        return
    
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
    Eliminar libros por nombre
    """
    book = search_books(bd,name)
    if book:
        bd.remove(book)
        print("Libro eliminado.")
    else:
        print("No se encontro el producto.")

def assign_books(bd, bd_assign, name, custum, amount, date, discount):
    """
    Registra la venta de un libro, asociando cliente, cantidad, fecha y descuento.
    Valida y actualiza el stock disponible automáticamente.
    """
    # 1. Buscar el libro para obtener sus detalles y stock
    book = search_books(bd, name)
    # Esta validación es por seguridad, aunque app.py ya lo comprueba.
    if not book:
        print(f"Error interno: El libro '{name}' no fue encontrado para la venta.")
        return

    # 2. Validar stock disponible
    if book['many'] < amount:
        print(f"Error: No hay suficiente stock para '{name}'. Disponible: {book['many']}, Solicitado: {amount}")
        return

    # 3. Actualizar el stock automáticamente
    book['many'] -= amount

    # 4. Registrar la venta en la base de datos de ventas
    total_price = (book['precio'] * amount)
    final_price = total_price - discount if discount is not None else total_price

    sale_record = {'title': name, 'customer': custum, 'amount': amount, 'date': date, 'discount': discount, 'final_price': final_price}
    bd_assign.append(sale_record)
    print(f"Venta registrada exitosamente. Stock actualizado para '{name}': {book['many']} unidades restantes.")

def list_assign_books(bd_assign):
    """
    mostrar la lista de libros existentes en formato legible.
    """
    if not bd_assign:
        print("No hay Libros registrados.")
        return

    print("\n=== LISTA DE PRODUCTOS ===")
    for book in bd_assign:
        print(f"Libro: {book["title"]} | Cliente: {book["customer"]} | Cantidad: {book["amount"]} | Fecha de la venta: {book["date"]} | Precio final: ${book["final_price"]}")

def calculate_report_data(bd, bd_assign):
    """
    Calcula todos los datos necesarios para los reportes a partir de las ventas.
    Retorna un diccionario con los datos procesados o None si no hay ventas.
    """
    if not bd_assign:
        return None
    

    # 1. Unidades vendidas por libro
    sold_count = {}
    for sale in bd_assign:
        title = sale['title']
        amount = sale['amount']
        sold_count[title] = sold_count.get(title, 0) + amount

    # 2. Ventas totales (ingresos netos) por autor
    sales_by_author = {}
    for sale in bd_assign:
        book = search_books(bd, sale['title'])
        if book:
            author = book['author']
            sales_by_author[author] = sales_by_author.get(author, 0) + sale['final_price']

    # 3. Ingreso neto y bruto
    net_income = sum(sale['final_price'] for sale in bd_assign)
    total_discounts = sum(sale.get('discount', 0.0) for sale in bd_assign)
    gross_income = net_income + total_discounts

    # 4. Ranking de libros más vendidos (de mayor a menor)
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
    Mostrar los calculos realizados en "def calculate_report_data(bd, bd_assign):"
    de forma legible para el usuario.
    """
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