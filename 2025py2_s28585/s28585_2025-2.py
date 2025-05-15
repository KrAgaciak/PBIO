from Bio import Entrez, SeqIO
import pandas as pd
import matplotlib.pyplot as plt
import time

print("NCBI GenBank Retriever")
email = input("Email: ")
api_key = input("API key: ")
taxid = input("TaxID: ")
try:
    min_len = int(input("Min length: "))
    max_len = int(input("Max length: "))
except:
    print("Invalid input.")
    exit()

Entrez.email = email
Entrez.api_key = api_key
Entrez.tool = "GenBankScript"

try:
    Entrez.efetch(db="taxonomy", id=taxid, retmode="xml").close()
    h = Entrez.esearch(db="nucleotide", term=f"txid{taxid}[Organism]", usehistory="y")
    r = Entrez.read(h)
    webenv, query_key, count = r["WebEnv"], r["QueryKey"], int(r["Count"])
except Exception as e:
    print("Search error:", e)
    exit()

records, fetched, batch, max_recs = [], 0, 200, 100
for start in range(0, count, batch):
    if fetched >= max_recs: break
    try:
        h = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",
                          retstart=start, retmax=batch, webenv=webenv, query_key=query_key)
        for rec in SeqIO.parse(h, "genbank"):
            l = len(rec.seq)
            if min_len <= l <= max_len:
                records.append({"accession": rec.id, "length": l, "description": rec.description})
                fetched += 1
                if fetched >= max_recs: break
        time.sleep(0.4)
    except Exception as e:
        print("Fetch error:", e)
if not records:
    print("No matching records.")
    exit()

csv_name = f"taxid_{taxid}_filtered.csv"
pd.DataFrame(records).to_csv(csv_name, index=False)
print(f"CSV saved to {csv_name}")

plot_name = f"taxid_{taxid}_plot.png"
df = pd.DataFrame(records).sort_values(by='length', ascending=False)
plt.figure(figsize=(10, 5))
plt.plot(df["accession"], df["length"], marker='o')
plt.xticks(rotation=90)
plt.xlabel("Accession"); plt.ylabel("Length"); plt.title("Sequence Lengths")
plt.tight_layout(); plt.savefig(plot_name); plt.close()
print(f"Plot saved to {plot_name}")