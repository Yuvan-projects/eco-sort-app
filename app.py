import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Universal Barcode Lookup", page_icon="📦", layout="centered"
)

st.title("📦 Universal Barcode Lookup")
st.write(
    "Type any product barcode number (food or non-food) to fetch details and"
    " get recycling advice."
)

# Sidebar for API Key Configuration
st.sidebar.header("⚙️ API Configuration")
api_key = st.sidebar.text_input(
    "Product API Key (e.g. Go-UPC)", type="password", value="HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
)

# Main Barcode Typing Input
barcode_input = st.text_input(
    "Enter Barcode Number:", placeholder="e.g. 8904132956728"
)


def lookup_universal_barcode(code, key):
  # Using Go-UPC API endpoint structure
  url = f"https://go-upc.com/api/v1/code/{code}"
  headers = {"Authorization": f"Bearer {key}"}

  req = urllib.request.Request(url, headers=headers)
  try:
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode("utf-8"))
      product = data.get("product", {})
      return product.get("name"), product.get("description")
  except Exception as e:
    return None, None


if st.button("Lookup Product"):
  if barcode_input:
    clean_code = barcode_input.strip()

    if not clean_code.isdigit():
      st.error("Please enter numbers only for the barcode.")
    elif not api_key:
      st.error("Please enter your Product API Key in the sidebar first!")
    else:
      with st.spinner("Querying universal database..."):
        product_name, description = lookup_universal_barcode(clean_code, api_key)

        if product_name:
          st.success(f"**Product Found:** {product_name}")
          if description:
            st.write(f"**Description:** {description}")

          st.markdown("### 📋 Disposal Guidance")
          st.write(
              "• **Rigid Containers / Bottles:** Rinse and place in curbside"
              " recycling.\n"
              "• **Soft Plastic Packaging / Wrappers:** Drop off at local"
              " grocery collection bins or place in landfill.\n"
              "• **Cardboard / Paper Boxes:** Flatten and put in paper"
              " recycling."
          )
        else:
          st.warning(
              "Product not found for this barcode in the universal database."
          )
  else:
    st.warning("Please type a barcode number first.")