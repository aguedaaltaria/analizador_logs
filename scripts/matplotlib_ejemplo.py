import matplotlib.pyplot as plt

# 1. Datos
categorias = ["/inicio", "/login", "/panel"]
visitas = [6, 11, 11]

# 2. Crear el lienzo (ancho=6 pulgadas, alto=4 pulgadas)
plt.figure(figsize=(6, 4))

# 3. Dibujar las barras
plt.bar(categorias, visitas, color="skyblue")

# 4. Personalizar textos y ejes
plt.title("Visitas por Endpoint")
plt.xlabel("Ruta")
plt.ylabel("Cantidad de Solicitudes")

# 5. Guardar o mostrar
plt.tight_layout()  # Ajusta los márgenes automáticamente para que no se corte texto
plt.savefig("mi_primer_grafico.png", dpi=300)
plt.close()  # Cierra la figura para liberar memoria RAM