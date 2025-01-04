
import pandas as pd
import streamlit as st
from datetime import datetime

# Initialize the client database
def initialize_database():
    return pd.DataFrame(columns=["Client Name", "Contract Type", "Status", "Start Date", "End Date", "Notes"])

# Add a new client contract
def add_contract(database, client_name, contract_type, status, start_date, end_date, notes):
    new_row = {
        "Client Name": client_name,
        "Contract Type": contract_type,
        "Status": status,
        "Start Date": start_date,
        "End Date": end_date,
        "Notes": notes,
    }
    return database.append(new_row, ignore_index=True)

# Streamlit application
st.title("Gestion des Contrats Clients")

# Initialize or load the database
if "database" not in st.session_state:
    st.session_state["database"] = initialize_database()

database = st.session_state["database"]

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Ajouter un contrat", "Liste des contrats", "Modifier les contrats"])

# Tab 1: Add a new contract
with tab1:
    st.header("Ajouter un nouveau contrat")

    client_name = st.text_input("Nom du client")
    contract_type = st.selectbox("Type de contrat", [
        "Assurance maladie",
        "Assurance de garantie des biens et de la fortune",
        "Prévoyance",
        "Constitution de la fortune",
        "Immobilier",
    ])
    status = st.selectbox("Statut", ["Signé", "Non signé"])
    start_date = st.date_input("Date de début", datetime.now())
    end_date = st.date_input("Date de fin")
    notes = st.text_area("Notes")

    if st.button("Ajouter le contrat"):
        database = add_contract(database, client_name, contract_type, status, start_date, end_date, notes)
        st.session_state["database"] = database
        st.success(f"Contrat ajouté pour {client_name}.")

# Tab 2: View all contracts
with tab2:
    st.header("Liste des contrats")
    if database.empty:
        st.info("Aucun contrat enregistré.")
    else:
        st.dataframe(database)

# Tab 3: Modify contracts
with tab3:
    st.header("Modifier ou supprimer des contrats")
    if database.empty():
        st.info("Aucun contrat à modifier ou supprimer.")
    else:
        contract_to_modify = st.selectbox("Sélectionnez un contrat à modifier", database.index)
        if st.button("Supprimer le contrat"):
            database = database.drop(contract_to_modify).reset_index(drop=True)
            st.session_state["database"] = database
            st.success("Contrat supprimé.")
        else:
            client_name = st.text_input("Nom du client", value=database.loc[contract_to_modify, "Client Name"])
            contract_type = st.selectbox("Type de contrat", [
                "Assurance maladie",
                "Assurance de garantie des biens et de la fortune",
                "Prévoyance",
                "Constitution de la fortune",
                "Immobilier",
            ], index=[
                "Assurance maladie",
                "Assurance de garantie des biens et de la fortune",
                "Prévoyance",
                "Constitution de la fortune",
                "Immobilier",
            ].index(database.loc[contract_to_modify, "Contract Type"]))
            status = st.selectbox("Statut", ["Signé", "Non signé"], index=["Signé", "Non signé"].index(database.loc[contract_to_modify, "Status"]))
            start_date = st.date_input("Date de début", database.loc[contract_to_modify, "Start Date"])
            end_date = st.date_input("Date de fin", database.loc[contract_to_modify, "End Date"])
            notes = st.text_area("Notes", value=database.loc[contract_to_modify, "Notes"])

            if st.button("Mettre à jour le contrat"):
                database.loc[contract_to_modify] = {
                    "Client Name": client_name,
                    "Contract Type": contract_type,
                    "Status": status,
                    "Start Date": start_date,
                    "End Date": end_date,
                    "Notes": notes,
                }
                st.session_state["database"] = database
                st.success("Contrat mis à jour avec succès.")
