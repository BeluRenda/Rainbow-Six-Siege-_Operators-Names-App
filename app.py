import os
from tkinter import Tk, Label, Entry, Button, Canvas, Frame
from PIL import Image, ImageTk, ImageDraw, ImageFont

class RainbowSixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rainbow Six Siege - Nombrador de Operadores")
        self.root.geometry("800x600")  # Tam de la ventana
        self.root.configure(bg="#2E2E2E")  # Color del fondo

        # Frame para la imagen y el nombre
        self.image_frame = Frame(root, bg="#2E2E2E")
        self.image_frame.pack(pady=20)

        self.image_label = Label(self.image_frame, bg="#2E2E2E")
        self.image_label.pack()

        # Frame para el nombre y los botones
        self.control_frame = Frame(root, bg="#2E2E2E")
        self.control_frame.pack(pady=20)

        self.name_entry = Entry(self.control_frame, font=("Arial", 16), width=30)
        self.name_entry.pack(side='left', padx=10)

        self.submit_button = Button(self.control_frame, text="Elegir nombre", command=self.set_name, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.submit_button.pack(side='left', padx=10)

        self.prev_button = Button(self.control_frame, text="Anterior", command=self.previous_operator, bg="#2196F3", fg="white", font=("Arial", 14))
        self.prev_button.pack(side='left', padx=10)

        self.next_button = Button(self.control_frame, text="Siguiente", command=self.next_operator, bg="#2196F3", fg="white", font=("Arial", 14))
        self.next_button.pack(side='left', padx=10)

        self.canvas = Canvas(root, width=600, height=400, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack()

        self.operators = self.load_images("images")
        self.current_operator_index = 0
        self.operator_names = {}  # Diccionario para guardar los nombres de los operadores
        self.display_operator()

        # Vincula tecla 'Enter' a la func set_name
        self.name_entry.bind('<Return>', self.set_name_on_enter)

    def load_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                images.append(os.path.join(folder, filename))
        return images

    def display_operator(self):
        if self.operators:
            image_path = self.operators[self.current_operator_index]
            name = self.operator_names.get(image_path, "")  # Obtiene el nombre guardado o vacío
            self.name_entry.delete(0, 'end')  # Limpia el campo de entrada
            self.name_entry.insert(0, name)  # Inserta el nombre guardado
            self.show_image(image_path)

    def show_image(self, image_path):
        image = Image.open(image_path)
        name = self.name_entry.get()
        self.add_text_to_image(image, name)

    def add_text_to_image(self, image, text):
        draw = ImageDraw.Draw(image)
        
        # Carga la fuente TrueType 
        font_size = 40  
        font_path = "arial.ttf"  
        font = ImageFont.truetype(font_path, font_size)
        
        # Cuadro delimitador del texto
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        width, height = image.size

        # Agrega el texto centrado en la parte inferior de la imagen
        x = (width - text_width) / 2
        y = height - text_height - 10 
        draw.text((x, y), text, fill="white", font=font)

        # Convertir a PhotoImage y mostrar
        self.display_photo(image)

    def display_photo(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def set_name(self):
        current_operator = self.operators[self.current_operator_index]
        name = self.name_entry.get()
        self.operator_names[current_operator] = name  # Guardar el nombre en el diccionario
        self.display_operator()

    def set_name_on_enter(self, event):
        self.set_name()  # Llama a la func set_name se apreta la tecla Enter

    def next_operator(self):
        if self.operators:
            self.current_operator_index = (self.current_operator_index + 1) % len(self.operators)
            self.display_operator()

    def previous_operator(self):
        if self.operators:
            self.current_operator_index = (self.current_operator_index - 1) % len(self.operators)
            self.display_operator()

if __name__ == "__main__":
    root = Tk()
    app = RainbowSixApp(root)
    root.mainloop()