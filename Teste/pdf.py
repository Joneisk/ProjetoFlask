import pypdfium2 as pdfium
from pathlib import Path
from PIL import Image
import img2pdf
import os

nome_pdf = "CASAMENTO.pdf"
nome_pdf_comprimido = "comprimido.pdf"
nome_pdf_sem_extensao = Path(nome_pdf).stem
escala = 2  # Escala para converter PDF em imagem

# Extrair cada página do PDF como imagem
pdf = pdfium.PdfDocument(nome_pdf)
quantidade_paginas = len(pdf)
imagens = []
for indice_pagina in range(quantidade_paginas):
    numero_pagina = indice_pagina + 1
    nome_imagem = f"{nome_pdf_sem_extensao}_{numero_pagina}.jpg"
    imagens.append(nome_imagem)
    print(f"Extraindo página {numero_pagina} de {quantidade_paginas}")
    pagina = pdf.get_page(indice_pagina)
    imagem_para_pil = pagina.render(scale=escala).to_pil()
    imagem_para_pil.save(nome_imagem)

imagens_comprimidas = []
# Comprimir imagens.
# Quanto menor a qualidade, menor o peso do PDF resultante
qualidade = 95
for nome_imagem in imagens:
    print(f"Comprimindo {nome_imagem}...")
    nome_imagem_sem_extensao = Path(nome_imagem).stem
    nome_imagem_saida = nome_imagem_sem_extensao + \
        "_comprimida" + nome_imagem[nome_imagem.rfind("."):]
    imagem = Image.open(nome_imagem)
    imagem.save(nome_imagem_saida, optimize=True, quality=qualidade)
    imagens_comprimidas.append(nome_imagem_saida)

# Escrever imagens em um novo PDF
print("Criando PDF comprimido...")
with open(nome_pdf_comprimido, "wb") as documento:
    documento.write(img2pdf.convert(imagens_comprimidas))

# Eliminar imagens temporárias
for imagem in imagens + imagens_comprimidas:
    os.remove(imagem)
