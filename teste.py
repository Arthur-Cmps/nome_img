import os
from tkinter import Tk, filedialog, Label, Button, Entry, StringVar, messagebox
from PIL import Image, ImageDraw, ImageFont

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_origem.set(pasta)

def processar_imagens():
    input_folder = pasta_origem.get()
    if not input_folder:
        messagebox.showerror("Erro", "Selecione a pasta com as imagens.")
        return

    nome_marca = texto_marca.get()
    if not nome_marca:
        messagebox.showerror("Erro", "Digite o texto a ser adicionado.")
        return

    output_folder = os.path.join(input_folder, "Imagens Marcadas")
    os.makedirs(output_folder, exist_ok=True)

    font_path = "C:/Windows/Fonts/arial.ttf"
    font_size = 36
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 0)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            image = Image.open(img_path).convert("RGBA")

            txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            bbox = draw.textbbox((0, 0), nome_marca, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (image.width - text_width) / 2
            y = 10

            draw.text((x, y), nome_marca, font=font, fill=text_color)

            combined = Image.alpha_composite(image, txt_layer)
            combined = combined.convert("RGB")
            output_path = os.path.join(output_folder, filename)
            combined.save(output_path)

    messagebox.showinfo("Concluído", f"✅ Todas as imagens foram processadas e salvas em:\n{output_folder}")

# Interface com Tkinter
app = Tk()
app.title("Adicionador de Texto em Imagens")
app.geometry("500x220")

pasta_origem = StringVar()
texto_marca = StringVar()
texto_marca.set("Proc 201674300583 Mand 202574300475")

Label(app, text="1. Selecione a pasta com imagens:").pack(pady=5)
Button(app, text="Selecionar Pasta", command=selecionar_pasta).pack()
Label(app, textvariable=pasta_origem, fg="blue").pack(pady=5)

Label(app, text="2. Texto a adicionar nas imagens:").pack()
Entry(app, textvariable=texto_marca, width=50).pack(pady=5)

Button(app, text="Iniciar Processamento", command=processar_imagens, bg="green", fg="white").pack(pady=10)

app.mainloop()