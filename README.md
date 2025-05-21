
# 💊 MedMais – Sistema de Gerenciamento de Estoque de Medicamentos

Sistema web completo para controle de medicamentos, fornecedores e lotes, desenvolvido com **Flask (Python)** e **MySQL**. Ideal para farmácias, clínicas ou hospitais que desejam organizar e acompanhar entradas, saídas e validade de produtos farmacêuticos.

---

## 🚀 Funcionalidades

- ✅ Cadastro, edição e exclusão de medicamentos
- ✅ Cadastro de fornecedores com CNPJ e contato
- ✅ Controle de lotes com data de entrada, validade e quantidade
- ✅ Relacionamento entre medicamentos e fornecedores
- ✅ Interface limpa com Bootstrap
- ✅ Confirmação de exclusão por prompt
- ✅ Separação por rotas e templates com Jinja2

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [MySQL](https://www.mysql.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Jinja2](https://jinja.palletsprojects.com/)

---

## 📦 Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/rafgam10/MedMais---Gerencimento-de-Estoque-para-Remedio-
cd medmais-estoque
```

2. **Crie um ambiente virtual e ative:**

```bash
python3 -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados:**

- Crie o banco de dados `gerenciamento_de_estoque` no MySQL.
- Execute o script SQL de criação das tabelas (fornecido na pasta `/sql/`).
- Insira dados fictícios se desejar com o script `dados_iniciais.sql`.

5. **Configure a conexão com o banco:**

Edite a função `conectar_banco()` no `app.py` com suas credenciais:

```python
mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="gerenciamento_de_estoque"
)
```

---

## ▶️ Executando o Projeto

```bash
python app.py
```

Acesse no navegador: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📁 Estrutura do Projeto

```
medmais-estoque/
│
├── app.py
├── db_config.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── fornecedor.html
│   ├── medicamentos.html
│   ├── lote.html
│   ├── cadastroFornecedor.html
│   ├── cadastroMedicamento.html
│   ├── cadastroLote.html
│   ├── relatorio.html
├── static/
│   └── (estilos e ícones, opcional)
├── requirements.txt
├── env/
└── README.md
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie sua branch com a feature (`git checkout -b minha-feature`)
3. Commit suas alterações (`git commit -m 'feat: nova funcionalidade'`)
4. Push para a branch (`git push origin minha-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Desenvolvido por **[Rafael Timóteo]**  


