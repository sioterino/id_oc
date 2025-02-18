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
    seq_num = tutor_id.count(half)
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
    seq_num = cat_id.count(half)
    half = half + str(seq_num)
    security = mod(half)
    return half + str(security)


cat_nome = cats_df["nome"].tolist()
cat_cor = cats_df["raca"].tolist()
cat_idade = cats_df["idade"].tolist()
cat_sexo = cats_df["sexo"].tolist()
cat_tags = cats_df["tags"].tolist()

cat_tutor = cats_df["tutor"].tolist()
cat_email = cats_df["email"].tolist()
cat_telefone = cats_df["telefone"].tolist()


for i in range(len(cats_df)):
    tutor_id.append(tutor(cat_tutor[i]))


for i in range(0, rows):
    cat_id.append(id_cat(i))


tutor_json = {
    "id": tutor_id,
    "nome": cat_tutor,
    "email": cat_email,
    "telefone": cat_telefone
}

cats_json = []

for i in range(rows):
    cat_json = {
        "id": cat_id[i],
        "nome": cat_nome[i],
        "raca": cat_cor[i],
        "idade": cat_idade[i],
        "sexo": cat_sexo[i],
        "tutor": {
            "id": tutor_id[i],
            "nome": cat_tutor[i],
            "email": cat_email[i],
            "telefone": cat_telefone[i]
        },
        "personalidade": eval(cat_tags[i])
    }
    cats_json.append(cat_json)

df = pd.DataFrame(cats_json)
df.to_json("cats.json", orient="records", indent=4, force_ascii=False)
