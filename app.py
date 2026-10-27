import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Eco-Sort Recycler", page_icon="♻️", layout="centered"
)

st.title("♻️ Eco-Sort & Recycle")
st.write(
    "Scan a barcode or type an item name (e.g., plastic pouch, cardboard box) to"
    " get disposal advice!"
)

# Accepts either a barcode number or a text description
query_input = st.text_input("Enter Barcode or Item Name:")

st.write("Or take a photo of the item:")
camera_image = st.camera_input("Take a picture")

if camera_image is not None:
  st.success("Photo captured!")


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
    return None


def ask_hugging_face(item_description):
  api_token = "HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
  model_id = "meta-llama/Llama-3-8B-Instruct"
  url = f"https://api-inference.huggingface.co/models/{model_id}"

  headers = {
      "Authorization": f"Bearer {api_token}",
      "Content-Type": "application/json",
  }
  prompt = (
      f"The item is '{item_description}'. Is this item Compostable,"
      " Recyclable, or Landfill? Give a brief disposal rule."
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
  if query_input:
    clean_query = query_input.strip()
    with st.spinner("Analyzing item with AI..."):

      # If it's a barcode, try looking it up in Open Food Facts first
      if clean_query.isdigit() and len(clean_query) >= 8:
        product_name = lookup_product_by_barcode(clean_query)
        if product_name:
          st.success(f"Found Product: **{product_name}**")
          item_to_check = product_name
        else:
          # Fallback: If not in food database, let the AI evaluate it directly
          st.info(
              "Barcode not in food database. Consulting AI for recycling"
              " guidance..."
          )
          item_to_check = f"Household packaging item (barcode {clean_query})"
      else:
        # User typed a text description directly
        item_to_check = clean_query

      advice = ask_hugging_face(item_to_check)
      st.markdown("### 📋 Disposal Guidance")
      st.write(advice)
  else:
    st.warning("Please enter a barcode or item name first.")