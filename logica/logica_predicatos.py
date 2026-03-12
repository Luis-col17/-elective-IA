productos = [{"nombre": "Pan", "stock": 10, "tipo": "Basico"}, 
            {"nombre": "Reloj", "stock": 0, "tipo": "Lujo"}]

tiene_stock=all(producto["stock"] > 0 for producto in productos)
print("sin stock en: ", [producto["nombre"] for producto in productos if producto["stock"] == 0])
print(tiene_stock) 

cat_lujo=any(producto["tipo"] == "Lujo" for producto in productos)
print("Productos de lujo: ", [producto["nombre"] for producto in productos if producto["tipo"] == "Lujo"])
print(cat_lujo)