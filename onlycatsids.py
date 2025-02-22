import random
import pandas as pd


cats_df = pd.read_csv("./onlycats.csv")
rows = len(cats_df)

cat_id = []
tutor_id = []

tutor_nome = {}


def tutor(nome):
    if nome in tutor_nome:
        return tutor_nome[nome]

    default_num = 7
    rand5 = random.randint(10000, 99999)
    half = "0" + str(default_num) + str(rand5)
    seq_num = sum(1 for num in tutor_id if num[:-2] == half)
    half = half + str(seq_num)
    security = mod(half)

    new_tutor_id = half + str(security)

    tutor_nome[nome] = new_tutor_id
    return new_tutor_id


def mod(str):
    sum = 0
    weight = 2
    for _, val in enumerate(str):
        sum += int(val) * weight
        weight = (weight % 9) + 1
    return (11 - sum % 11) % 10


def id_cat(i):
    default_num = "08"
    tutor = tutor_id[i][2:]
    sexo = "1" if cat_sexo[i] == "Macho" else "0"
    cor = "9"
    match cat_cor[i]:
        case "Preto":
            cor = "1"
        case "Branco":
            cor = "2"
        case "Cinza":
            cor = "3"
        case "Castanho":
            cor = "4"
        case "Laranja":
            cor = "5"
        case "Tigrado":
            cor = "6"
        case "Bicolor":
            cor = "7"
        case "Tricolor":
            cor = "8"

    half = default_num + tutor + sexo + cor
    seq_num = sum(1 for num in cat_id if num[:-2] == half)
    half = half + str(seq_num)
    security = mod(half)
    return half + str(security)


cats_df["cadastro"] = pd.to_datetime(cats_df["cadastro"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
cat_cad = cats_df["cadastro"].tolist()
cat_nome = cats_df["nome"].tolist()
cat_cat = cats_df["gato"].tolist()
cat_cor = cats_df["raca"].tolist()
cat_idade = cats_df["idade"].tolist()
cat_sexo = cats_df["sexo"].tolist()
cat_tags = cats_df["tags"].tolist()

cat_tutor = cats_df["tutor"].tolist()
tutor_composto = cats_df["composto"].tolist()
cat_email = cats_df["email"].tolist()
cat_telefone = cats_df["telefone"].tolist()

cat_img_num = cats_df["imagens"].tolist()
cat_img_path = []


for i in range(len(cats_df)):
    tutor_id.append(tutor(cat_tutor[i].strip()))


for i in range(0, rows):
    cat_id.append(id_cat(i))


cat_pop = []

for i in range(0, rows):
    cat_pop.append(random.randint(100, 6000))

tutor_given_names = []
tutor_surnames = []

for i in range(rows):
    full_name = cat_tutor[i].strip().split()

    if tutor_composto[i]:
        given_name = full_name[:2]
        surname = full_name[2:]
    else:
        given_name = full_name[:1]
        surname = full_name[1:]

    tutor_given_names.append(given_name)
    tutor_surnames.append(surname)

for i in range(0, rows):
    paths = []
    for j in range(0, cat_img_num[i]):
        paths.append(f"../img/gatos/{tutor_given_names[i][0].lower()}-{'-'.join(str(cat_nome[i]).strip().lower().split())}-{j}")
    cat_img_path.append(paths)

cats_json = []

for i in range(rows):
    cat_json = {
        "id": cat_id[i],
        "cadastro": cat_cad[i],
        "popularidade": cat_pop[i],
        "nome": cat_nome[i],
        "isCat": cat_cat[i],
        "raca": cat_cor[i],
        "idade": cat_idade[i],
        "sexo": cat_sexo[i],
        "tutor": {
            "id": tutor_id[i],
            "nome": tutor_given_names[i],
            "sobrenome": tutor_surnames[i],
            "email": cat_email[i],
            "telefone": cat_telefone[i]
        },
        "personalidade": eval(cat_tags[i]),
        "imgPath": cat_img_path[i]
    }
    cats_json.append(cat_json)

df = pd.DataFrame(cats_json)
df.to_json("E:/code/projeto-2-cabrita/json/cats.json", orient="records", indent=4, force_ascii=False)

def has_duplicates(arr):
    # Convert the list to a set and compare lengths
    return len(arr) != len(set(arr))


for i in range(0, rows):
    print(f"Tutor: {cat_tutor[i]} | Cat: {cat_nome[i]} | Cat ID: {cat_id[i]}")
    # print(f"{cat_tutor[i]} : {tutor_id[i]}")
    pass

# Check for duplicates
print(f"\n\n{has_duplicates(tutor_id)}")
