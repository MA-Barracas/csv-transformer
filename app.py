import streamlit as st
import pandas as pd



# Function to rename columns
def rename_columns(df):
    df.columns = ['Renamed_Column1', 'Renamed_Column2', 'Renamed_Column3']
    return df

# Function to create a new ratio column
def create_ratio_column(df, col1, col2):
    df['Ratio_Column'] = df[col1] / df[col2]
    return df

# Function to process the CSV file
def process_csv(df, apply_rename, apply_ratio):
      
        # Apply selected processing functions
    if apply_rename:
        df = rename_columns(df)
    if apply_ratio:
        if 'Renamed_Column1' in df.columns and 'Renamed_Column2' in df.columns:
            df = create_ratio_column(df, 'Renamed_Column1', 'Renamed_Column2')
        else:
            st.warning("Cannot create Ratio Column: Ensure that 'Renamed_Column1' and 'Renamed_Column2' exist.")
    
    return df

# Streamlit app layout
st.set_page_config(page_title="CSV Processor App", page_icon="📊", layout="wide")

# Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 50 !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("CSV Processor Options")
st.sidebar.markdown("Use this app to upload a CSV file, process it, and download the modified version.")

# Main content
st.title("📊 CSV Processor App")
st.markdown("""
    This app allows you to upload a CSV file and apply a series of transformations to it. 
    The columns in your CSV will be renamed and a new ratio column will be added, 
    based on the values in two of your existing columns.
    """)

# File uploader
st.subheader("Step 2: Upload Your CSV File")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Make sure your CSV has at least two columns.")

st.sidebar.subheader("Step 1: Select the CSV Separator")
separator = st.sidebar.selectbox(
            "Choose the separator used in your CSV file:",
            options=["comma", "semi-colon", "pipe", "whitespace"],
            index=0,
            help="Select the character that separates columns in your CSV file."
        )

sep_map = {"comma": ",", "semi-colon": ";","pipe": "|","whitespace": " "}
separator = sep_map[separator]

if uploaded_file is not None:
    st.success("CSV file uploaded successfully!")
    
    # Display the uploaded file
    st.subheader("Step 3: Preview Uploaded File")
    st.write("Here's a preview of your uploaded file:")

    

    original_df = pd.read_csv(uploaded_file, sep=separator)
    st.dataframe(original_df)

    # Processing options
    st.subheader("Step 4: Select Processing Options")
    apply_rename = st.radio(
        "Do you want to rename the columns?",
        options=["Yes", "No"],
        index=0,
        help="Select 'Yes' to rename the columns in the CSV file."
    ) == "Yes"
    
    apply_ratio = st.radio(
        "Do you want to create a ratio column?",
        options=["Yes", "No"],
        index=0,
        help="Select 'Yes' to create a new column with the ratio of two existing columns."
    ) == "Yes"
    

    # Process the uploaded file
    st.subheader("Step 5: Process the File")
    if st.button("Process CSV", help="Click to process the CSV file"):
        processed_df = process_csv(original_df, apply_rename, apply_ratio)
        st.success("CSV file processed successfully!")
        
        # Display the processed DataFrame
        st.write("Here's a preview of your processed file:")
        st.dataframe(processed_df)
        
        # Provide a download link for the processed file
        processed_file = processed_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Processed CSV",
            data=processed_file,
            file_name='processed_data.csv',
            mime='text/csv',
            help="Click to download the processed CSV file."
        )
else:
    st.warning("Please upload a CSV file to proceed.")
    
# Footer
st.sidebar.markdown("---")
st.sidebar.info("Created with ❤️ for Dami.")

st.sidebar.image("hibot.png", caption="EDEM - 2024 🏫")
