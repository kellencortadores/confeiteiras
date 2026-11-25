# cadastro_confeiteiras.py
# Python 3.x
#
# Cadastro simples de confeiteiras com Tkinter
# Salva em clientes_instagram.json
# Gera automaticamente clientes.html com busca, cards em ordem alfabética e botão para copiar lista do WhatsApp

import json
import os
import webbrowser
from tkinter import *
from tkinter import ttk, messagebox

ARQUIVO_JSON = "Confeiteiras Parceiras.json"
ARQUIVO_HTML = "Confeiteiras Parceiras.html"


# =========================
# JSON
# =========================
def carregar_clientes():
    if not os.path.exists(ARQUIVO_JSON):
        return []

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def salvar_clientes(clientes):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4)


# =========================
# HTML
# =========================
def gerar_html():
    clientes = carregar_clientes()
    
    # Ordena as clientes por nome (sem diferenciar maiúsculas/minúsculas)
    clientes_ordenados = sorted(clientes, key=lambda c: c["nome"].lower())

    cards = ""

    for cliente in clientes_ordenados:
        nome = cliente["nome"]
        instagram = cliente["instagram"]
        url = cliente["url_instagram"]

        cards += f"""
        <div class="card" data-nome="{nome}" data-insta="@{instagram}" data-search="{nome.lower()} {instagram.lower()}">
            <h2>🧁 {nome}</h2>

            <p>
                <strong>Instagram:</strong>
                @{instagram}
            </p>

            <a href="{url}" target="_blank" class="botao">
                Abrir Instagram
            </a>
        </div>
        """

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Confeiteiras Parceiras</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #fff5f7;
    margin: 0;
    padding: 30px;
}}

header {{
    text-align: center;
    margin-bottom: 20px;
}}

h1 {{
    color: #c45c7a;
    margin-bottom: 5px;
}}

.subtitulo {{
    color: #666;
    margin-bottom: 20px;
}}

.acoes {{
    text-align: center;
    margin-bottom: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}}

.busca input {{
    width: 350px;
    max-width: 90%;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #ddd;
    font-size: 16px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}}

.btn-whatsapp {{
    background: #25D366;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
    transition: background 0.2s, transform 0.1s;
}}

.btn-whatsapp:hover {{
    background: #1ebd59;
    transform: translateY(-2px);
}}

.btn-whatsapp:active {{
    transform: translateY(0);
}}

.container {{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}}

.card {{
    background: white;
    width: 280px;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.10);
    transition: transform 0.2s;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card h2 {{
    color: #b24d6b;
    font-size: 20px;
    margin-top: 0;
}}

.botao {{
    display: inline-block;
    margin-top: 15px;
    background: #d86b8c;
    color: white;
    padding: 10px 16px;
    border-radius: 10px;
    text-decoration: none;
}}

.botao:hover {{
    background: #c45c7a;
}}

.sem-resultados {{
    text-align: center;
    color: #777;
    margin-top: 30px;
}}
</style>

</head>

<body>

<header>
    <h1>🍰 Confeiteiras Parceiras</h1>
    <div class="subtitulo">
        Catálogo de clientes do Instagram
    </div>
</header>

<div class="acoes">
    <div class="busca">
        <input
            type="text"
            id="pesquisa"
            placeholder="🔍 Buscar por nome ou Instagram..."
            onkeyup="filtrar()"
        >
    </div>
    <button class="btn-whatsapp" onclick="copiarListaWhatsApp()">
        📋 Copiar Lista para WhatsApp
    </button>
</div>

<div class="container" id="cards">
    {cards}
</div>

<p class="sem-resultados" id="mensagem" style="display:none;">
    Nenhuma confeiteira encontrada.
</p>

<script>
function filtrar() {{
    let termo = document
        .getElementById("pesquisa")
        .value
        .toLowerCase();

    let cards = document.querySelectorAll(".card");

    let encontrou = false;

    cards.forEach(function(card) {{
        let texto = card.dataset.search;

        if (texto.includes(termo)) {{
            card.style.display = "block";
            encontrou = true;
        }} else {{
            card.style.display = "none";
        }}
    }});

    document.getElementById("mensagem").style.display =
        encontrou ? "none" : "block";
}}

function copiarListaWhatsApp() {{
    let cards = document.querySelectorAll(".card");
    let textoFinal = "*🍰 EVOLUÇÃO DA NOSSA LISTA DE PARCEIRAS 🍰*\\n\\n";
    let contador = 0;

    cards.forEach(function(card) {{
        // Só adiciona na lista se o card estiver visível no momento
        if (card.style.display !== "none") {{
            let nome = card.dataset.nome;
            let insta = card.dataset.insta;
            contador++;
            textoFinal += contador + ") *" + nome + "* - " + insta + "\\n";
        }}
    }});

    if (contador === 0) {{
        alert("Nenhuma confeiteira na lista para copiar!");
        return;
    }}

    textoFinal += "\\n✨ Venha fazer parte você também!";

    // Copia para a área de transferência usando a API do navegador
    navigator.clipboard.writeText(textoFinal).then(function() {{
        alert("📋 Lista copiada com sucesso! Agora é só dar Ctrl+V (ou colar) no WhatsApp.");
    }}).catch(function(err) {{
        alert("Erro ao copiar texto: " + err);
    }});
}}
</script>

</body>
</html>
"""

    with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
        f.write(html)


# =========================
# Cadastro
# =========================
def cadastrar():
    nome = entrada_nome.get().strip()
    insta = entrada_instagram.get().strip()

    if not nome:
        messagebox.showwarning(
            "Atenção",
            "Informe o nome."
        )
        return

    if not insta:
        messagebox.showwarning(
            "Atenção",
            "Informe o Instagram."
        )
        return

    # aceita URL completa ou usuário
    if "instagram.com" in insta.lower():
        url = insta.rstrip("/")

        usuario = url.split("/")[-1]
    else:
        usuario = insta.replace("@", "")
        url = f"https://www.instagram.com/{usuario}/"

    clientes = carregar_clientes()

    novo_id = (
        max([c["id"] for c in clientes], default=0)
        + 1
    )

    clientes.append({
        "id": novo_id,
        "nome": nome,
        "instagram": usuario,
        "url_instagram": url
    })

    salvar_clientes(clientes)
    gerar_html()

    entrada_nome.delete(0, END)
    entrada_instagram.delete(0, END)

    messagebox.showinfo(
        "Sucesso",
        "Cliente cadastrada!\nHTML atualizado."
    )


def abrir_html():
    gerar_html()

    caminho = os.path.abspath(ARQUIVO_HTML)

    webbrowser.open("file://" + caminho)


# =========================
# Interface
# =========================
janela = Tk()
janela.title("🍰 Cadastro de Confeiteiras")
janela.geometry("450x280")
janela.resizable(False, False)

frame = ttk.Frame(janela, padding=25)
frame.pack(fill="both", expand=True)

titulo = Label(
    frame,
    text="🍰 Cadastro de Confeiteiras",
    font=("Arial", 18, "bold"),
    fg="#b24d6b"
)
titulo.pack(pady=(0, 20))


Label(
    frame,
    text="Nome"
).pack(anchor="w")

entrada_nome = Entry(
    frame,
    font=("Arial", 11)
)
entrada_nome.pack(
    fill="x",
    pady=(0, 15)
)


Label(
    frame,
    text="Instagram (usuário ou URL)"
).pack(anchor="w")

entrada_instagram = Entry(
    frame,
    font=("Arial", 11)
)
entrada_instagram.pack(
    fill="x",
    pady=(0, 20)
)


Button(
    frame,
    text="Salvar",
    bg="#d86b8c",
    fg="white",
    font=("Arial", 11, "bold"),
    command=cadastrar
).pack(fill="x")


Button(
    frame,
    text="Abrir catálogo HTML",
    command=abrir_html
).pack(
    fill="x",
    pady=(10, 0)
)


# gera HTML inicial caso já exista JSON
gerar_html()

janela.mainloop()
