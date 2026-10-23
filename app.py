import json
import urllib.request
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Eco-Sort Recycler", page_icon="♻️", layout="centered"
)

st.title("♻️ Eco-Sort & Recycle")
st.write(
    "Scan or enter a product barcode to find out how to dispose of it properly!"
)

# Input field (mobile keyboards automatically switch to numeric mode for barcodes)
barcode = st.text_input("Enter Barcode Number:")

# Optional: Camera input for mobile users
st.write("Or take a photo of the item:")
camera_image = st.camera_input("Take a picture")

if camera_image is not None:
  st.success("Photo captured! (Tip: Enter the barcode number above to lookup)")


def lookup_product_by_barcode(code):
  url = f"https://world.openfoodfacts.org/api/v0/product/{code}.json"
  req = urllib.request.Request(
      url, headers={"User-Agent": "EcoSortApp - Streamlit - Version 1.0"}
  )
  try:
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode("utf-8"))
      if data.get("status") == 1:
        return data.get("product", {}).get("product_name", "Unknown Product")
      return None
  except Exception as e:
    st.error(f"Lookup Error: {e}")
    return None


def ask_hugging_face(product_name):
  # Replace with your actual Hugging Face API Token if needed
  api_token = "HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
  model_id = "meta-llama/Llama-3-8B-Instruct"
  url = f"https://api-inference.huggingface.co/models/{model_id}"

  headers = {
      "Authorization": f"Bearer {api_token}",
      "Content-Type": "application/json",
  }
  prompt = (
      f"The product is '{product_name}'. Is this item Compostable, Recyclable,"
      " or Landfill? Give a brief disposal rule."
  )
  payload = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}

  req = urllib.request.Request(
      url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
  )
  try:
    with urllib.request.urlopen(req) as response:
      result = json.loads(response.read().decode("utf-8"))
      if isinstance(result, list) and len(result) > 0:
        return result[0].get("generated_text", "No response text found.")
      return str(result)
  except Exception as e:
    return f"AI Error: {e}"


if st.button("Get Recycling Advice"):
  if barcode:
    with st.spinner("Looking up product and consulting AI..."):
      product_name = lookup_product_by_barcode(barcode)

      if product_name:
        st.success(f"Found Product: **{product_name}**")
        advice = ask_hugging_face(product_name)

        st.markdown("### 📋 Disposal Guidance")
        st.write(advice)
      else:
        st.warning(
            "Product not found for this barcode. Try entering another one!"
        )
  else:
    st.warning("Please enter a barcode number first.")