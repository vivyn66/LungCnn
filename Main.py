import tensorflow as tf
import numpy as np

from tkinter import *
import os
from tkinter import filedialog
import cv2
import time
from matplotlib import pyplot as plt
from tkinter import messagebox


def endprogram():
    print("\nProgram terminated!")
    sys.exit()


def file_sucess():
    global file_success_screen
    file_success_screen = Toplevel(training_screen)
    file_success_screen.title("File Upload Success")
    file_success_screen.geometry("150x100")
    file_success_screen.configure(bg='cyan')
    Label(file_success_screen, text="File Upload Success").pack()
    Button(file_success_screen, text='''ok''', font=(
        'Verdana', 15), height="2", width="30", bg='cyan').pack()


global ttype


def training():
    global training_screen

    global clicked

    training_screen = Toplevel(main_screen)
    training_screen.title("Training")
    # login_screen.geometry("400x300")
    training_screen.geometry("600x450+650+150")
    training_screen.minsize(120, 1)
    training_screen.maxsize(1604, 881)
    training_screen.resizable(1, 1)
    training_screen.configure(bg='cyan')
    # login_screen.title("New Toplevel")

    Label(training_screen, text='''Upload Image ''', background="#d9d9d9", disabledforeground="#a3a3a3",
          foreground="#000000", width="300", height="2", bg='cyan', font=("Calibri", 16)).pack()
    Label(training_screen, text="").pack()

    options = [
        "Covid",
        "Influenza",
        "Normal",
        "Pneumonia",
        "Tuberculosis"

    ]

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set("LungDisease ")

    # Create Dropdown menu
    drop = OptionMenu(training_screen, clicked, *options)
    drop.config(width="30", bg='cyan')

    drop.pack()

    ttype = clicked.get()

    Button(training_screen, text='''Upload Image''', font=(
        'Verdana', 15), height="2", width="30", bg='cyan', command=imgtraining).pack()


def imgtraining():
    name1 = clicked.get()

    print(name1)

    import_file_path = filedialog.askopenfilename()
    import os
    s = import_file_path
    os.path.split(s)
    os.path.split(s)[1]
    splname = os.path.split(s)[1]

    image = cv2.imread(import_file_path)
    # filename = 'Test.jpg'
    filename = 'Data/' + name1 + '/' + splname

    cv2.imwrite(filename, image)
    print("After saving image:")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Original image', image)
    cv2.imshow('Gray image', gray)
    # import_file_path = filedialog.askopenfilename()
    print(import_file_path)
    fnm = os.path.basename(import_file_path)
    print(os.path.basename(import_file_path))

    from PIL import Image, ImageOps

    im = Image.open(import_file_path)
    im_invert = ImageOps.invert(im)
    im_invert.save('lena_invert.jpg', quality=95)
    im = Image.open(import_file_path).convert('RGB')
    im_invert = ImageOps.invert(im)
    im_invert.save('tt.png')
    image2 = cv2.imread('tt.png')
    cv2.imshow("Invert", image2)

    """"-----------------------------------------------"""

    img = image

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Original image', img)
    # cv2.imshow('Gray image', gray)
    # dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    dst = cv2.medianBlur(img, 7)
    cv2.imshow("Nosie Removal", dst)


def fulltraining():
    import model as mm


def testing():
    global testing_screen
    testing_screen = Toplevel(main_screen)
    testing_screen.title("Testing")
    # login_screen.geometry("400x300")
    testing_screen.geometry("600x450+650+150")
    testing_screen.minsize(120, 1)
    testing_screen.maxsize(1604, 881)
    testing_screen.resizable(1, 1)
    testing_screen.configure(bg='cyan')
    # login_screen.title("New Toplevel")

    Label(testing_screen, text='''Upload Image''', disabledforeground="#a3a3a3",
          foreground="#000000", width="300", height="2", bg='cyan', font=("Calibri", 16)).pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Button(testing_screen, text='''Upload Image''', font=(
        'Verdana', 15), height="2", width="30", bg='cyan', command=imgtest).pack()


global affect


def imgtest():
    import_file_path = filedialog.askopenfilename()

    image = cv2.imread(import_file_path)
    print(import_file_path)
    filename = 'Output/Out/Test.jpg'
    cv2.imwrite(filename, image)
    print("After saving image:")
    # result()

    # import_file_path = filedialog.askopenfilename()
    print(import_file_path)
    fnm = os.path.basename(import_file_path)
    print(os.path.basename(import_file_path))

    # file_sucess()

    print("\n*********************\nImage : " + fnm + "\n*********************")
    img = cv2.imread(import_file_path)
    if img is None:
        print('no data')

    img1 = cv2.imread(import_file_path)
    print(img.shape)
    img = cv2.resize(img, ((int)(img.shape[1] / 5), (int)(img.shape[0] / 5)))
    original = img.copy()
    neworiginal = img.copy()
    cv2.imshow('original', img1)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    img1S = cv2.resize(img1, (960, 540))

    cv2.imshow('Original image', img1S)
    grayS = cv2.resize(gray, (960, 540))
    cv2.imshow('Gray image', grayS)

    dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
    cv2.imshow("Nosie Removal", dst)

    thresh = 127
    im_bw = cv2.threshold(grayS, thresh, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("affect Removal", im_bw)
    number_of_black_pix = np.sum(im_bw == 0)
    # print(number_of_black_pix)
    # if(number_of_black_pix<5000):
    # affect =

    result()


def result():
    import warnings
    warnings.filterwarnings('ignore')

    import tensorflow as tf
    classifierLoad = tf.keras.models.load_model('lungmodel.h5')

    import numpy as np
    from keras.preprocessing import image

    test_image = image.load_img('Output/Out/Test.jpg', target_size=(200, 200))
    img1 = cv2.imread('Output/Out/Test.jpg')
    # test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifierLoad.predict(test_image)

    out = ''
    pre = ''
    if result[0][0] == 1:
        print("Covid")
        out = "Covid"
        pre = "Ivermectin, Hydroxychloroquine"
    elif result[0][1] == 1:
        print("Influenza")
        out = "Influenza"
        pre = "Flucelvax Quadrivalent (Seqirus)	5.0-mL MDV"
    elif result[0][2] == 1:
        print("Normal")
        out = "Normal"
        pre = " "
    elif result[0][3] == 1:
        print("Pneumonia")
        out = "Pneumonia"
        pre = "levofloxacin, clarithromycin"

    elif result[0][4] == 1:
        print("Tuberculosis")
        out = "Tuberculosis"
        pre = "isoniazid / pyrazinamide / rifampin"

    messagebox.showinfo("Result", "Classification Result : " + str(out))

    messagebox.showinfo("prescription", "prescription : " + str(pre))


def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.configure(bg='cyan')
    main_screen.title("Lung Disease Prediction ")

    Label(text="Lung Disease Prediction", width="300", height="5", bg='cyan', font=("Calibri", 16)).pack()

    Button(text="UploadImage", font=(
        'Verdana', 15), height="2", width="30", command=training, highlightcolor="black", bg='cyan').pack(side=TOP)
    Label(text="").pack()
    Button(text="Training", font=(
        'Verdana', 15), height="2", width="30", command=fulltraining, highlightcolor="black", bg='cyan').pack(side=TOP)

    Label(text="").pack()
    Button(text="Testing", font=(
        'Verdana', 15), height="2", width="30", bg='cyan', command=testing).pack(side=TOP)

    Label(text="").pack()

    main_screen.mainloop()


main_account_screen()
