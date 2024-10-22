from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Gemini API with the provided API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get a response
def get_gemini_response(input_prompt, image_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

# Function to handle image upload and return image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button for submitting the analysis
submit = st.button("Tell me the total calories")

# Input prompt for the Gemini AI model
input_prompt = """
You are an expert nutritionist. Analyze the food items from the image 
and calculate the total calories. Provide the details of each food item with 
caloric intake in the following format:

1. Item 1 - number of calories - Nutritious (Yes/No) - Health benefits
2. Item 2 - number of calories - Nutritious (Yes/No) - Health benefits
...
Total calories: [total calories]

Additionally, provide the recommended daily intake for an average adult and specify 
if these food items contribute positively to a healthy diet. Are they suitable for a balanced diet?
"""

# If submit button is clicked
if submit:
    try:
        # Set up image data for processing
        image_data = input_image_setup(uploaded_file)
        
        # Get response from Gemini API
        response = get_gemini_response(input_prompt, image_data)
        
        # Display the response
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
