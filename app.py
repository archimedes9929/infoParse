import streamlit as st
import tabula
import pandas as pd
import os, sys
import tempfile
from io import BytesIO

FILEPATH = os.path.realpath(__file__)
FILEDIR  = os.path.dirname(FILEPATH)
inputs_dir  = os.path.join(FILEDIR, "inputs")
outputs_dir = os.path.join(FILEDIR, "outputs")

st.title("Tabular PDF to XLSX conversion")

to_convert = st.file_uploader("Upload a PDF file with tables", type="pdf")

@st.cache_data
def to_xlsx_bytes(df:pd.DataFrame, output_path:str) -> bytes:
    out_df.to_excel(output_path, index=False)
    with open(output_path, "rb") as template_file:
        xl_bytes = template_file.read()
        return xl_bytes

if to_convert is not None:

    file_name = os.path.basename(to_convert.name)
    # Define the full path to the file

    file_path = os.path.join(inputs_dir, file_name)
     # Save the file
    with open(file_path, 'wb') as f:
        f.write(to_convert.getvalue())

    st.write("File successfully uploaded. Locally stored")

    # Grab from local
    pages = tabula.read_pdf(file_path, pages="all")
    for page in pages[1:]: page.columns = pages[0].columns
    out_df:pd.DataFrame = pd.concat(pages)

    # Convert into Excel File
    output_filename = file_name.split(".")[0]+".xlsx"

    output_path = os.path.join(outputs_dir, output_filename)
    st.write(output_filename)
    xl_bytes = to_xlsx_bytes(out_df, output_path)

    # # Read out_df.xlsx and download
    st.download_button(
        label="Download output file",
        data=xl_bytes,
        file_name=output_filename,
        mime='application/octet-stream',
    )