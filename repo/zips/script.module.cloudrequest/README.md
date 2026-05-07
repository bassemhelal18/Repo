# CloudRequest

**Versão:** 1.0.2  
**Desenvolvido por:** oneplay team

---

## Sobre

CloudRequest é uma biblioteca HTTP leve e poderosa para Kodi que fornece uma sessão **CloudScraper** com bypass automático do Cloudflare (incluindo o desafio IUAM - "I'm Under Attack Mode").

Permite que addons Kodi acessem sites protegidos pelo Cloudflare de forma transparente, sem interrupções ou bloqueios.

---

## Recursos

- Bypass automático de desafios Cloudflare IUAM, v2, v3 e Turnstile
- Compatível com a API do `requests`
- **Interpretador JavaScript próprio** — sem dependências externas de runtime JS
- Implementado 100% em Python
- Leve e otimizado para Kodi

---

## Como usar

```python
from cloudrequest import CloudRequest

# Cria uma sessão com bypass Cloudflare
session = CloudRequest().get_session()

# Faça requisições normalmente, como se fosse o requests
response = session.get("https://site-protegido.com")
print(response.text)
```

A sessão retornada é totalmente compatível com a API do `requests`:

```python
session = CloudRequest().get_session()

# GET com parâmetros
response = session.get("https://site-protegido.com/api", params={"q": "busca"})

# POST com dados
response = session.post("https://site-protegido.com/login", data={"user": "x", "pass": "y"})

# Acessando cookies e headers da resposta
print(response.status_code)
print(response.cookies)
```

---

## Arquitetura interna

```
cloudscraper/
├── __init__.py                  # Núcleo do cloudscraper
├── cloudflare.py                # Handler IUAM v1
├── cloudflare_v2.py             # Handler IUAM v2
├── cloudflare_v3.py             # Handler JS VM v3
├── turnstile.py                 # Handler Turnstile
├── stealth.py                   # Técnicas anti-detecção
├── http_inspector.py            # Inspetor HTTP (substitui requests-toolbelt)
├── help.py                      # Diagnóstico do ambiente
└── interpreters/
    ├── __init__.py              # JavaScriptInterpreter + NativeInterpreter
    └── js_engine.py             # Motor JS puro em Python
```

O `js_engine.py` implementa o subconjunto ES5/ES6 necessário para resolver os desafios Cloudflare:

- Coerção de tipos JS (`+[]`, `!+[]`, `[]+{}`, etc.)
- Escopos léxicos, closures, arrow functions
- Operadores bitwise, `typeof`, `instanceof`
- Built-ins: `Math`, `JSON`, `Array`, `String`, `Object`, `Number`, `atob/btoa`, `parseInt`, `console`, `Date.now`

---

## 🏆 Créditos Especiais

---

### 🕷️ cloudscraper — VeNoMouS

> **Repositório:** [github.com/VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper)

O **cloudscraper** é a espinha dorsal deste módulo. Construído sobre o `requests`, ele implementa toda a lógica de detecção e bypass de proteções Cloudflare — do clássico IUAM ao moderno Turnstile.

Sem o **VeNoMouS**, bypass de Cloudflare em Python seria um pesadelo. 🎩

---

### 🧠 js2py — Piotr Dabkowski *(inspiração)*

> **Repositório:** [github.com/PiotrDabkowski/Js2Py](https://github.com/PiotrDabkowski/Js2Py)

O **js2py** foi a inspiração original para a abordagem de interpretar JavaScript diretamente em Python. A partir da v1.0.2, o CloudRequest não depende mais do js2py como biblioteca instalada — o engine é próprio e embutido. 🙌

---

## 📄 Licenças de Dependências

| Biblioteca | Autor | Licença | Link |
|---|---|---|---|
| [cloudscraper](https://github.com/VeNoMouS/cloudscraper) | VeNoMouS | MIT | [Ver licença](https://opensource.org/licenses/MIT) |

---

*Feito com ❤️ pela **oneplay team***
