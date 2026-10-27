import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Eco-Sort Recycler", page_icon="♻️", layout="centered"
)

st.title("♻️ Eco-Sort & Recycle")
st.write(
    "Type any product barcode number or item name to get instant disposal"
    " advice!"
)

# Sidebar for optional API configuration
st.sidebar.header("⚙️ API Configuration")
api_key = st.sidebar.text_input(
    "Product API Key (Optional)", type="password", value="HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
)

# Main typing input (handles both barcodes and item names)
query_input = st.text_input(
    "Enter Barcode Number or Item Name:", placeholder="e.g. 8904132956728"
)


def lookup_api_barcode(code, key):
  if not key:
    return None
  url = f"https://go-upc.com/api/v1/code/{code}"
  headers = {"Authorization": f"Bearer {key}"}
  req = urllib.request.Request(url, headers=headers)
  try:
    with urllib.request.urlopen(req, timeout=5) as response:
      data = json.loads(response.read().decode("utf-8"))
      product = data.get("product", {})
      return product.get("name")
  except Exception:
    return None


def get_local_advice(query):
  item_lower = query.lower()

  if "plastic" in item_lower or "pouch" in item_lower or "wrapper" in item_lower:
    return (
        "**Soft Plastic / Pouch**: Flexible plastic films and pouches cannot go"
        " in standard curbside bins. Check local grocery store drop-off bins"
        " or place in landfill."
    )
  elif "cardboard" in item_lower or "box" in item_lower:
    return (
        "**Cardboard / Paper**: Flatten the clean box completely and place it"
        " in your paper recycling bin."
    )
  elif "glass" in item_lower or "bottle" in item_lower:
    return (
        "**Glass**: Rinse out any remaining liquid and place in glass recycling."
    )
  elif "can" in item_lower or "tin" in item_lower or "aluminum" in item_lower:
    return (
        "**Metal**: Rinse lightly and place in your metal recycling bin."
    )
  else:
    return (
        f"**General Guidance for '{query}'**: If clean and made of rigid"
        " plastic, paper, or metal, it is usually recyclable. When in doubt,"
        " place in Landfill to avoid contaminating other recyclables."
    )


if st.button("Get Recycling Advice"):
  if query_input:
    clean_query = query_input.strip()
    product_name = None

    with st.spinner("Analyzing item..."):
      # If the input is a barcode (numbers only)
      if clean_query.isdigit():
        if api_key:
          product_name = lookup_api_barcode(clean_query, api_key)

        if product_name:
          st.success(f"**Product Found:** {product_name}")
          item_to_check = product_name
        else:
          st.info(
              "Barcode not found in external database. Using smart material"
              " fallback..."
          )
          item_to_check = f"Barcode {clean_query}"
      else:
        # If the input is a text description
        item_to_check = clean_query

      # Fetch and display recycling advice
      advice = get_local_advice(item_to_check)
      st.markdown("### 📋 Disposal Guidance")
      st.write(advice)
  else:
    st.warning("Please enter a barcode number or item name first.")