import streamlit as st
import hashlib
import time

# Initialize the blockchain list
blockchain = []

# Function to create a block
def create_block(index, data, previous_hash):
    block = {
        "index": index,
        "data": data,
        "timestamp": time.time(),
        "previous_hash": previous_hash
    }
    return block

# Function to generate a unique hash for each block
def generate_hash(block):
    block_string = f"{block['index']}{block['data']}{block['timestamp']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Function to add a new recharge record
def add_recharge_record(customer_name, mobile_number, operator, amount):
    previous_block = blockchain[-1]  # Get the last block
    new_index = previous_block["index"] + 1  # New block index
    new_hash = generate_hash(previous_block)  # Hash of the last block

    # Create recharge data
    recharge_data = {
        "customer_name": customer_name,
        "mobile_number": mobile_number,
        "operator": operator,
        "amount": amount
    }

    # Create a new block with recharge data
    new_block = create_block(new_index, recharge_data, new_hash)
    blockchain.append(new_block)

# Create Genesis block if blockchain is empty
if not blockchain:
    genesis_block = create_block(1, "Genesis Block", "0")
    blockchain.append(genesis_block)

# Streamlit app layout
st.title("📱 Mobile Recharge Blockchain")

st.header("🔗 Add a New Mobile Recharge")

with st.form("recharge_form"):
    customer_name = st.text_input("Customer Name")
    mobile_number = st.text_input("Mobile Number")
    operator = st.selectbox("Operator", ["Airtel", "Jio", "Vi", "BSNL"])
    amount = st.number_input("Recharge Amount", min_value=1, step=1)
    submit = st.form_submit_button("Add Recharge")

    if submit:
        if customer_name and mobile_number and operator and amount > 0:
            add_recharge_record(customer_name, mobile_number, operator, amount)
            st.success(f"Recharge added for {customer_name}!")
        else:
            st.error("Please fill all fields correctly.")

# Display the blockchain
st.header("📜 Mobile Recharge Blockchain")

for block in blockchain:
    with st.expander(f"Block Index: {block['index']}"):
        st.write("Recharge Data:", block["data"])
        st.write("Timestamp:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block["timestamp"])))
        st.write("Previous Hash:", block["previous_hash"])
