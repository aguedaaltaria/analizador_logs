import matplotlib.pyplot as plt
import seaborn as sns

# 1. Aplicar tema visual moderno
sns.set_theme(style="whitegrid")

# 2. Datos
codigos = ["HTTP 200", "HTTP 403", "HTTP 500"]
totales = [27, 10, 7]

# 3. Matplotlib prepara la figura
plt.figure(figsize=(7, 4))

# 4. Seaborn dibuja las barras con una paleta degradada
sns.barplot(x=codigos, y=totales, palette="viridis", hue=codigos, legend=False)

# 5. Matplotlib añade los textos y guarda
plt.title("Códigos de Respuesta Web")
plt.xlabel("Estado HTTP")
plt.ylabel("Peticiones")

plt.savefig("grafico_seaborn.png", dpi=300)
plt.close()