import streamlit as st
from pdfminer.high_level import extract_text
import pandas as pd
import numpy as np
import re
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

root.wm_attributes('-topmost', 1)

st.title('Fuel consumption DDR evaluation')
clicked = st.button('Select Folder')

if clicked:

    dirname = filedialog.askdirectory(master=root)

    st.code(dirname)

    files = os.listdir(dirname)

    df = np.zeros((len(files), 2)).astype(object)

    for i in range(len(files)):

        file_path = dirname + r'\\' + files[i]
        pdf_read = extract_text(file_path)

        if str(re.search(rf"(Dieselverbrauch: )", pdf_read)) != 'None' and re.findall('[0-9]+', pdf_read[re.search(rf"(Dieselverbrauch: )", pdf_read).end():re.search(rf"(Dieselverbrauch: )", pdf_read).end() + 5]) != re.findall('[0-9]+', pdf_read[re.search(rf"(kum. Dieselverbrauch: )", pdf_read).end():re.search(rf"(kum. Dieselverbrauch: )", pdf_read).end()+6]):
            y = re.search(rf"(Dieselverbrauch: )", pdf_read)
            y_num = re.findall('[0-9]+', pdf_read[y.end(): y.end() + 5])
            df[i, 0] = float(y_num[0])
        if str(re.search(rf"(kum. Dieselverbrauch: )", pdf_read)) != 'None':
            x = re.search(rf"(kum. Dieselverbrauch: )", pdf_read)
            x_num = re.findall('[0-9]+', pdf_read[x.end(): x.end()+6])
            df[i, 1] = float(x_num[0])

    df = pd.DataFrame(df, columns=['Diesel consumption', 'cumulative Diesel consumption'])

    st.table(df)


