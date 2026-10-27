import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Eco-Sort Recycler", page_icon="♻️", layout="centered"
)

st.title("♻️ Eco-Sort & Recycle")
st.write("Get instant disposal advice using local rules or AI cloud models!")

# Sidebar Settings for Local vs. API Control
st.sidebar.header("⚙️ Engine Settings")
mode_choice = st.sidebar.radio(
    "Select Mode:", ("Hybrid (Smart Fallback)", "Local Rules Only", "AI API Only")
)
api_token_input = st.sidebar.text_input(
    "Hugging Face API Token", type="password", value="HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
)

# Main Inputs
query_input = st.text_input("Enter Item Name (e.g., plastic pouch, box):")
camera_image = st.camera_input("Take a picture")

if camera_image is not None:
  st.success("Photo captured!")


def get_local_advice(item):
  item_lower = item.lower()
  if "plastic" in item_lower or "pouch" in item_lower or "wrapper" in item_lower:
    return (
        "**[Local Engine] Recycler (Soft Plastic)**: Flexible pouches require"
        " special grocery store drop-off bins rather than standard curbside"
        " sorting."
    )
  elif "cardboard" in item_lower or "box" in item_lower:
    return (
        "**[Local Engine] Recycler (Cardboard)**: Flatten the clean box"
        " completely and place it in your paper/cardboard bin."
    )
  elif "glass" in item_lower or "bottle" in item_lower:
    return (
        "**[Local Engine] Recycler (Glass)**: Rinse thoroughly and place in"
        " glass recycling."
    )
  elif "can" in item_lower or "tin" in item_lower or "aluminum" in item_lower:
    return (
        "**[Local Engine] Recycler (Metal)**: Rinse lightly and place in your"
        " metal recycling bin."
    )
  else:
    return (
        f"**[Local Engine] General Guidance for '{item}'**: Check local"
        " municipal rules. If clean rigid plastic, paper, or metal, it is usually"
        " recyclable."
    )


def get_ai_advice(item, token):
  model_id = "meta-llama/Llama-3-8B-Instruct"
  url = f"https://api-inference.huggingface.co/models/{model_id}"
  headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
  }
  prompt = (
      f"The item is '{item}'. Is this item Compostable, Recyclable, or"
      " Landfill? Give a brief disposal rule."
  )
  payload = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}

  req = urllib.request.Request(
      url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
  )
  with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode("utf-8"))
    if isinstance(result, list) and len(result) > 0:
      return result[0].get("generated_text", "No response text found.")
    return str(result)


if st.button("Get Recycling Advice"):
  if query_input:
    clean_query = query_input.strip()
    advice = ""

    with st.spinner("Analyzing disposal method..."):
      if mode_choice == "Local Rules Only":
        advice = get_local_advice(clean_query)

      elif mode_choice == "AI API Only":
        if not api_token_input:
          st.error(
              "Please enter your Hugging Face API token in the sidebar settings"
              " first!"
          )
        else:
          try:
            advice = get_ai_advice(clean_query, api_token_input)
          except Exception as e:
            st.error(f"API Error: {e}")

      else:  # Hybrid Mode (Default)
        if api_token_input:
          try:
            advice = get_ai_advice(clean_query, api_token_input)
          except Exception:
            st.info(
                "Network/API unavailable. Seamlessly falling back to local"
                " rules..."
            )
            advice = get_local_advice(clean_query)
        else:
          advice = get_local_advice(clean_query)

    if advice:
      st.markdown("### 📋 Disposal Guidance")
      st.write(advice)
  else:
    st.warning("Please enter an item name first.")