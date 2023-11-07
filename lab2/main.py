import cv2 as cv
from tkinter import ttk, Tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


class ImageProcessingApp:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1600x840")

        self.image_labels = {}
        self.image_path = None
        self.create_interface()

    def run(self):
        self.root.mainloop()

    def ask_file(self):
        path = askopenfilename()
        self.image_path = path
        self.load_images()

        self.apply_simple_thresholding()
        self.apply_otsu_thresholding()
        self.apply_adaptive_thresholding()
        self.apply_median_filter()

        self.root.mainloop()

    def create_interface(self):
        # Create labels for the images
        label_original = ttk.Label(text="Original Image")
        label_simple_threshold = ttk.Label(text="Simple global thresholding")
        label_otsu_threshold = ttk.Label(text="Otsu's global thresholding")
        label_adaptive_threshold = ttk.Label(text="Adaptive thresholding")
        label_median_filter = ttk.Label(text="Median filter")
        choose_button = ttk.Button(
            None,
            text='Choose file',
            command=self.ask_file)
        choose_button.grid(row=1, column=1, rowspan=1, columnspan=1)

        label_original.place(x=100, y=10)
        label_simple_threshold.place(x=100, y=430)
        label_otsu_threshold.place(x=470, y=430)
        label_adaptive_threshold.place(x=840, y=430)
        label_median_filter.place(x=1210, y=430)

        # Create labels for the processed images
        self.image_labels["original"] = ttk.Label()
        self.image_labels["simple_threshold"] = ttk.Label()
        self.image_labels["otsu_threshold"] = ttk.Label()
        self.image_labels["adaptive_threshold"] = ttk.Label()
        self.image_labels["median_filter"] = ttk.Label()

        self.image_labels["original"].place(x=100, y=40, width=350, height=350)
        self.image_labels["simple_threshold"].place(x=100, y=460, width=350, height=350)
        self.image_labels["otsu_threshold"].place(x=470, y=460, width=350, height=350)
        self.image_labels["adaptive_threshold"].place(x=840, y=460, width=350, height=350)
        self.image_labels["median_filter"].place(x=1210, y=460, width=350, height=350)

    def load_images(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_tk = self.make_image(image)
        self.image_labels["original"].configure(image=image_tk)
        self.image_labels["original"].image = image_tk

    def make_image(self, image):
        return ImageTk.PhotoImage(Image.fromarray(image).resize((350, 350)))

    def apply_simple_thresholding(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        ret, image_simple_threshold = cv.threshold(image, 127, 255, cv.THRESH_BINARY)

        image_tk = self.make_image(image_simple_threshold)
        self.image_labels["simple_threshold"].configure(image=image_tk)
        self.image_labels["simple_threshold"].image = image_tk

    def apply_otsu_thresholding(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        ret, image_otsu_threshold = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        image_tk = self.make_image(image_otsu_threshold)
        self.image_labels["otsu_threshold"].configure(image=image_tk)
        self.image_labels["otsu_threshold"].image = image_tk

    def apply_adaptive_thresholding(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_adaptive_threshold = cv.adaptiveThreshold(
            image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2
        )
        image_tk = self.make_image(image_adaptive_threshold)
        self.image_labels["adaptive_threshold"].configure(image=image_tk)
        self.image_labels["adaptive_threshold"].image = image_tk

    def apply_median_filter(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_median = cv.medianBlur(image, 5)

        image_tk = self.make_image(image_median)
        self.image_labels["median_filter"].configure(image=image_tk)
        self.image_labels["median_filter"].image = image_tk


if __name__ == "__main__":
    app = ImageProcessingApp()
    app.run()
