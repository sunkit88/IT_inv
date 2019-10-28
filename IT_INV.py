import pandas as pd

it_inv_raw = pd.read_csv(".\IT_INV.csv")
fin_inv_raw = pd.read_csv(".\FIN_INV.csv")

it_inv = it_inv_raw[(it_inv_raw["Status (Phy.)"]=="Yes") & (it_inv_raw["Status (Fixed Asset)"] == "Yes")]
it_inv = it_inv[["Compand Code", "Asset Code", "Model", "Serial No.", "Location", "User"]]
it_inv["Asset Code"] = it_inv["Asset Code"].apply(int)
it_inv["Asset Code"] = "00000000" + it_inv["Asset Code"].apply(str)
it_inv["Asset Code"] = it_inv["Asset Code"].str[-8:]
it_inv["AssetCode"] = it_inv["Compand Code"].astype(str) + it_inv["Asset Code"].astype(str)
it_inv = it_inv.drop(columns=["Asset Code"])
it_inv = it_inv.reindex(columns=["AssetCode"] + list(it_inv.columns[:-1]))

fin_inv = fin_inv_raw[["Business Unit AM", "Asset ID", "Asset Description", "Custodian", "Department"]]
fin_inv["Asset ID"] = fin_inv["Asset ID"].str[-8:]
fin_inv["AssetCode"] = fin_inv["Business Unit AM"].astype(str) + fin_inv["Asset ID"].astype(str)
fin_inv = fin_inv.drop(columns=["Asset ID"])
fin_inv = fin_inv.reindex(columns=["AssetCode"] + list(fin_inv.columns[:-1]))
fin_inv = fin_inv[fin_inv["Business Unit AM"].isin(["DFMNM", "DFSNM", "FCGEM", "FCHIM", "FCHKM", "FCITM", "FHSTM", "FJERM", "FMACM", "FMEMM", "FPHXM", "FSAVM", "FSFOM", "FTJNM", "FVANM"])]

it_inv_inner = pd.merge(it_inv, fin_inv, on='AssetCode', how='left')
it_inv_inner.to_csv("it_inv_inner.csv", index=0)

fin_inv_inner = pd.merge(fin_inv, it_inv, on='AssetCode', how='left')
fin_inv_inner.to_csv("fin_inv_inner.csv", index=0)

