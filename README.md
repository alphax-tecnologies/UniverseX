# SPOTIFY FREE

> Para utilizar nosso serviço open-source, siga as instruções de instalação correspondentes ao seu dispositivo. Itens necessários: Terminal Linux + Navegador

## 📱 Celular — Android

### 1. Instale o Termux
Baixe o Termux pela [página oficial na Play Store](https://play.google.com/store/apps/details?id=com.termux). Se a versão não estiver disponível ou estiver desatualizada, consulte o [repositório oficial do Termux](https://github.com/termux/termux-app).

### 2. Instale as dependências

Abra o Termux e execute:

```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg git -y
pip install flask yt-dlp
termux-setup-storage
```

Quando solicitado, conceda a permissão de acesso aos arquivos para permitir que o aplicativo salve as músicas no armazenamento compartilhado.

### 3. Baixe o projeto

```bash
git clone https://github.com/alphax-tecnologies/UniverseX
cd UniverseX
```

### 4. Crie o atalho `spo`

Execute os comandos abaixo para adicionar uma função ao arquivo `.bashrc`:

```bash
touch ~/.bashrc
echo 'spo() { cd "$HOME/UniverseX" && python mobile.py; }' >> ~/.bashrc
source ~/.bashrc
```

**O que isso faz?**
- Cria o arquivo `.bashrc` caso ele ainda não exista.
- Adiciona a função `spo`, que entra na pasta do projeto e executa `mobile.py`.
- Carrega a configuração imediatamente.

### 5. Inicie o serviço

Agora, sempre que quiser iniciar o serviço, basta executar:

```bash
spo
```

**Observação:** o atalho pressupõe que o projeto esteja em `$HOME/UniverseX`. Se você clonou o repositório em outro diretório, ajuste o caminho na função.

---

## 🍎 Celular — iOS

No iOS, não existe suporte ao Termux. Uma alternativa é utilizar o [iSH Shell](https://ish.app/), que fornece um ambiente de terminal baseado em Alpine Linux.

### 1. Instale o iSH Shell

Baixe o aplicativo pela App Store e abra o terminal.

### 2. Instale as dependências disponíveis

```sh
apk update
apk add python3 py3-pip git bash
```

O suporte a `ffmpeg`, Flask e `yt-dlp` pode variar conforme a versão do ambiente. O iSH não é equivalente ao Termux e pode não executar todas as dependências do projeto.

### 3. Baixe o projeto

```sh
git clone https://github.com/alphax-tecnologies/UniverseX
cd UniverseX
```

### 4. Instale as dependências Python

Se o projeto oferecer um arquivo `requirements.txt`, tente instalá-lo em um ambiente virtual:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se alguma dependência nativa não for compatível com o iOS ou o iSH, será necessário utilizar um ambiente Linux remoto ou um computador.

### 5. Execute o serviço

```sh
python3 mobile.py
```

---

## 💻 Desktop — Linux

### 1. Instale os requisitos do sistema

Em distribuições baseadas em Debian ou Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip ffmpeg git -y
```

### 2. Baixe o projeto

```bash
git clone https://github.com/alphax-tecnologies/UniverseX
cd UniverseX
```

### 3. Crie o ambiente virtual e instale as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Inicie o serviço

```bash
python mobile.py
```

**Importante:** o ambiente virtual deve estar ativado antes de executar o programa, caso contrário as dependências instaladas nele não estarão disponíveis.

---

## 🖥️ Desktop — Windows

### 1. Instale os requisitos

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [FFmpeg](https://ffmpeg.org/download.html)

Durante a instalação do Python, marque a opção **Add Python to PATH**.

### 2. Baixe o projeto

Abra o PowerShell:

```powershell
git clone https://github.com/alphax-tecnologies/UniverseX
cd UniverseX
```

### 3. Crie o ambiente virtual e instale as dependências

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Inicie o serviço

```powershell
python mobile.py
```

Se o PowerShell bloquear a ativação do ambiente virtual, você pode executar o programa diretamente pelo interpretador do ambiente:

```powershell
.\.venv\Scripts\python.exe mobile.py
```

---

## ⚠️ Informações importantes

- No desktop, utilize o `requirements.txt` para manter as dependências do projeto centralizadas.
- No Android, o atalho `spo` permite iniciar o serviço sem precisar entrar manualmente na pasta do projeto.
- No iOS, a compatibilidade depende das limitações do ambiente e das bibliotecas utilizadas.
- Verifique os requisitos e as condições de uso dos serviços e das fontes de áudio utilizados pelo projeto.
