import streamlit as st
import pandas as pd
from datetime import datetime

# === CONFIGURAÇÃO DE ESTILO ===
st.set_page_config(layout="wide", page_title="Sistema de Orçamentos")

def local_css():
    st.markdown("""
    <style>
    body { font-size: 14px; }
    .servico-card {
        padding: 4px 8px;
        margin: 4px 0;
        background-color: #f4f4f4;
        border-left: 3px solid #999;
        font-size: 13px;
    }
    .servico-card p {
        margin: 0;
    }
    .servico-preco {
        font-weight: bold;
        color: #000;
        font-size: 13px;
    }
    .carrinho-item {
        font-size: 13px;
        padding: 3px 0;
        margin: 0;
        border-bottom: 1px solid #ccc;
    }
    .total-box {
        font-size: 13px;
        margin-top: 8px;
        background: #eee;
        color: #000;  /* <- ESSA LINHA RESOLVE O PROBLEMA */
        padding: 8px;
        border-radius: 4px;
    }
    .stButton>button {
        font-size: 13px !important;
        padding: 6px 10px;
        margin: 4px 0;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# === CARREGA A BASE DE DADOS ===
@st.cache_data
def carregar_base():
    # Cria um DataFrame de exemplo se 'knowledge_base.csv' não existir para fins de demonstração.
    # Em um ambiente de produção, certifique-se de que o arquivo CSV esteja presente.
    try:
        df = pd.read_csv("knowledge_base.csv")
    except FileNotFoundError:
        st.warning("Arquivo 'knowledge_base.csv' não encontrado. Usando dados de exemplo para demonstração.")
        # Dados fornecidos pelo usuário
        data = [
            {'serviço': 'Artes', 'preço': '30', 'descricao': 'Arte para post, stories, feed'},
            {'serviço': 'Vídeo institucional (-1min)', 'preço': '50', 'descricao': 'Vídeo institucional de até 1 minuto'},
            {'serviço': 'Vídeo institucional (até 2min)', 'preço': '60', 'descricao': 'Vídeo institucional de até 2 minutos'},
            {'serviço': 'Vídeo institucional (até 3min)', 'preço': '70', 'descricao': 'Vídeo institucional de até 3 minutos'},
            {'serviço': 'Vídeo institucional (até 4min)', 'preço': '80', 'descricao': 'Vídeo institucional de até 4 minutos'},
            {'serviço': 'Vídeo institucional (até 5min)', 'preço': '90', 'descricao': 'Vídeo institucional de até 5 minutos'},
            {'serviço': 'Vídeo institucional (até 6min)', 'preço': '100', 'descricao': 'Vídeo institucional de até 6 minutos'},
            {'serviço': 'Vídeo institucional (até 7min)', 'preço': '110', 'descricao': 'Vídeo institucional de até 7 minutos'},
            {'serviço': 'Vídeo institucional (acima de 7 minutos)', 'preço': '0', 'descricao': 'Solicitar orçamento'},
            {'serviço': 'Motion de até 1min', 'preço': '80', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 1min (com locução)', 'preço': '100', 'descricao': 'Com locução'},
            {'serviço': 'Motion de até 2min', 'preço': '100', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 2min (com locução)', 'preço': '120', 'descricao': 'Com locução'},
            {'serviço': 'Motion de até 3min', 'preço': '120', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 3min (com locução)', 'preço': '140', 'descricao': 'Com locução'},
            {'serviço': 'Motion de até 4min', 'preço': '140', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 4min (com locução)', 'preço': '160', 'descricao': 'Com locução'},
            {'serviço': 'Motion de até 5min', 'preço': '160', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 5min (com locução)', 'preço': '180', 'descricao': 'Com locução'},
            {'serviço': 'Motion de até 6min', 'preço': '180', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 6min (com locução)', 'preço': '200', 'descricao': 'Com locução'},
            {'serviço': 'Motion de até 7min', 'preço': '200', 'descricao': 'Sem locução'},
            {'serviço': 'Motion de até 7min (com locução)', 'preço': '220', 'descricao': 'Com locução'},
            {'serviço': 'Motion acima de 7 minutos', 'preço': '0', 'descricao': 'Solicitar orçamento'},
            {'serviço': 'Social Media', 'preço': '300', 'descricao': 'Gerenciamento de redes sociais. Valor por conta'},
            {'serviço': 'ID Visual sem MIV', 'preço': '1000', 'descricao': 'Logo, aplicação, papelaria, paleta de cores'},
            {'serviço': 'ID Visual com MIV', 'preço': '1500', 'descricao': 'Logo, aplicação, papelaria, paleta de cores, manual de identidade visual'},
            {'serviço': 'Apenas Logo e Cores', 'preço': 'R$400', 'descricao': 'Criação de logo e definição de paleta de cores.'},
            {'serviço': 'Apenas Tipografia', 'preço': 'R$150', 'descricao': 'Definição e aplicação de tipografia para a marca.'},
            {'serviço': 'Apenas Emblema', 'preço': 'R$150', 'descricao': 'Criação de emblema (símbolo) para a marca, assumindo logo já existente.'},
            {'serviço': 'Apenas Papelaria', 'preço': 'R$150', 'descricao': 'Design de cartão de visita, papel timbrado e outros itens de papelaria, assumindo logo já existente.'},
            {'serviço': 'Uniforme', 'preço': 'R$100', 'descricao': 'Design de uniforme com a identidade visual da marca.'}
        ]
        df = pd.DataFrame(data)
    
    # GARANTE QUE A COLUNA 'preço' É NUMÉRICA
    # Limpa o campo 'preço' removendo caracteres não numéricos e convertendo para float
    df['preço'] = df['preço'].astype(str) \
                             .str.replace(r'[^\d,.]', '', regex=True) \
                             .str.replace(',', '.', regex=False)
    df['preço'] = pd.to_numeric(df['preço'], errors='coerce')
    df['preço'] = df['preço'].fillna(0) # Preenche valores que não puderam ser convertidos com 0

    df['preco_unitario_pacote'] = df['descricao'].str.extract(r'R\$(\d+) por')
    df['preco_unitario_pacote'] = df['preco_unitario_pacote'].fillna(0).astype(float)
    df['quantidade_pacote'] = df['descricao'].str.extract(r'(\d+) [a-z]+ por')
    df['quantidade_pacote'] = df['quantidade_pacote'].fillna(1).astype(int)
    return df

df = carregar_base()


# === FUNÇÕES AUXILIARES ===
def formatar_preco(valor):
    """Formata um valor numérico para o formato de moeda brasileira."""
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_desconto(qtd_total):
    """Calcula o desconto baseado na quantidade total de itens no carrinho."""
    return min(10, qtd_total * 2)  # 2% por item, até 10%

# === SISTEMA DE CARRINHO ===
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

def adicionar_ao_carrinho(servico, preco, quantidade=1):
    """Adiciona um serviço ao carrinho ou atualiza sua quantidade se já existir."""
    for item in st.session_state.carrinho:
        if item['servico'] == servico:
            item['quantidade'] += quantidade
            return
    st.session_state.carrinho.append({
        'servico': servico,
        'preco': preco,
        'quantidade': quantidade
    })

def remover_do_carrinho(index):
    """Remove um item do carrinho pelo seu índice."""
    st.session_state.carrinho.pop(index)

def calcular_total():
    """Calcula o subtotal, desconto e total final do carrinho."""
    subtotal = sum(item['preco'] * item['quantidade'] for item in st.session_state.carrinho)
    qtd_total = sum(item['quantidade'] for item in st.session_state.carrinho)
    desconto = calcular_desconto(qtd_total)
    valor_desconto = subtotal * desconto / 100
    total = subtotal - valor_desconto
    return subtotal, desconto, valor_desconto, total

# === INTERFACE PRINCIPAL ===
st.title("🛒 Serviços Ogusta.br")
st.markdown(f"*Atualizado em {datetime.now().strftime('%d/%m/%Y')}*")

# Divide em duas colunas
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Serviços Disponíveis")
    
    # Agrupa serviços por categoria de forma mais explícita
    all_services = df['serviço'].tolist()
    
    categorias = {
        'Artes': [],
        'Vídeos': [],
        'Motion': [],
        'Fotografia': [], # Mantido para caso seja adicionado via CSV real
        'Social Media': [],
        'Identidade Visual': [],
        'Adicionais': [],
        'Outros': []
    }

    for service in all_services:
        if 'Artes' in service and 'Social Media' not in service:
            categorias['Artes'].append(service)
        elif 'Vídeo' in service:
            categorias['Vídeos'].append(service)
        elif 'Motion' in service:
            categorias['Motion'].append(service)
        elif 'Fotografia' in service: # Este será preenchido apenas se 'Fotografia' estiver no CSV real
            categorias['Fotografia'].append(service)
        elif 'Social Media' in service:
            categorias['Social Media'].append(service)
        elif 'ID Visual' in service or 'Logo' in service or 'Tipografia' in service or 'Emblema' in service or 'Papelaria' in service:
            categorias['Identidade Visual'].append(service)
        elif 'Uniforme' in service:
            categorias['Adicionais'].append(service)
        else:
            categorias['Outros'].append(service)
    
    # Ordena os serviços dentro de cada categoria
    for category, services_list in categorias.items():
        categorias[category] = sorted(services_list)

    # Limpa categorias vazias para não exibir expanders desnecessários
    categorias = {k: v for k, v in categorias.items() if v}

    for categoria, servicos in categorias.items():
        with st.expander(f"🎨 {categoria}"):
            for i, servico in enumerate(servicos):
                row = df[df['serviço'] == servico].iloc[0]
                with st.container():
                    st.markdown(f"""
                    <div class="servico-card">
                        <div class="servico-title"><b>{servico}</b></div>
                        <div class="servico-preco">{formatar_preco(row['preço'])}</div>
                        <div class="servico-desc">{row['descricao']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Ajusta o label da quantidade para serviços específicos
                    if 'min' in servico and ('Vídeo' in servico or 'Motion' in servico):
                        if 'acima de' in servico: # Para serviços com preço 0 para "Solicitar orçamento"
                            st.info("Para este serviço, por favor, solicite um orçamento personalizado.")
                            qtd = 0 # Define quantidade como 0 para não permitir adicionar
                        else:
                            qtd_label = "Quantidade"
                            qtd = st.number_input(qtd_label, 
                                                min_value=1, 
                                                max_value=100, 
                                                value=1,
                                                key=f"qtd_{i}_{servico}")
                    elif servico == 'Fotografia':
                        qtd_label = "Quantidade de sessões de Fotografia"
                        qtd = st.number_input(qtd_label, 
                                            min_value=1, 
                                            max_value=100, 
                                            value=1,
                                            key=f"qtd_{i}_{servico}")
                    elif servico == 'Artes':
                         qtd_label = "Quantidade de artes"
                         qtd = st.number_input(qtd_label, 
                                            min_value=1, 
                                            max_value=100, 
                                            value=1,
                                            key=f"qtd_{i}_{servico}")
                    elif 'Social Media' in servico:
                         qtd_label = "Quantidade de meses"
                         qtd = st.number_input(qtd_label, 
                                            min_value=1, 
                                            max_value=100, 
                                            value=1,
                                            key=f"qtd_{i}_{servico}")
                    else:
                        qtd_label = f"Quantidade de {servico}"
                        qtd = st.number_input(qtd_label, 
                                            min_value=1, 
                                            max_value=100, 
                                            value=1,
                                            key=f"qtd_{i}_{servico}")
                    
                    # Oculta o botão "Adicionar" se o preço for 0 (solicitar orçamento)
                    if row['preço'] > 0:
                        if st.button(f"Adicionar {servico}", key=f"add_{i}_{servico}"):
                            adicionar_ao_carrinho(servico, row['preço'], qtd)
                            st.success(f"{qtd}x {servico} adicionado ao carrinho!")
                    else:
                        st.markdown(f"**{servico}:** Por favor, entre em contato para um orçamento personalizado.")


with col2:
    st.subheader("🛒 Carrinho")
    
    if not st.session_state.carrinho:
        st.info("Carrinho vazio.")
    else:
        for i, item in enumerate(st.session_state.carrinho):
            st.markdown(
                f"<div class='carrinho-item'>"
                f"{item['servico']} — {item['quantidade']}× {formatar_preco(item['preco'])} "
                f"= <b>{formatar_preco(item['preco'] * item['quantidade'])}</b>"
                f"</div>",
                unsafe_allow_html=True
            )
            # Coloca o botão de remover ao lado do item do carrinho
            col_item_desc, col_item_btn = st.columns([0.8, 0.2])
            with col_item_btn:
                if st.button("🗑", key=f"remover_{i}"):
                    remover_do_carrinho(i)
                    st.rerun()
        
        subtotal, desconto, valor_desconto, total = calcular_total()
        
        st.markdown(f"""
        <div class='total-box'>
        Subtotal: {formatar_preco(subtotal)}  
        <br>Desconto ({desconto}%): -{formatar_preco(valor_desconto)}  
        <br><b>Total: {formatar_preco(total)}</b>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão Limpar Carrinho no final do carrinho
        st.button("🔄 Limpar Carrinho", on_click=lambda: st.session_state.update({"carrinho": []}))

# === RODAPÉ ===
st.markdown("---")
st.markdown("Dúvidas? Entre em contato com nosso time comercial.")