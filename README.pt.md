# DAMN VULNERABLE WEB APPLICATION

Damn Vulnerable Web Application (DVWA) é um aplicativo web em PHP/MySQL que é extremamente vulnerável. Seu principal objetivo é auxiliar profissionais de segurança a testar suas habilidades e ferramentas em um ambiente legal, ajudar desenvolvedores web a entender melhor os processos de segurança de aplicações web e auxiliar tanto estudantes quanto professores a aprender sobre segurança de aplicações web em um entorno controlado em sala de aula.

O objetivo do DVWA é permitir a prática de algumas das vulnerabilidades web mais comuns, com vários níveis de dificuldade, por meio de uma interface simples e direta.
Tenha em mente que existem vulnerabilidades documentadas e não documentadas neste software. Isso é intencional. Encorajamos você a tentar descobrir o maior número possível de problemas.
- - -

## AVISO!

DVWA é muito vulnerável! **Não a carregue na pasta pública html do seu provedor de hospedagem ou em qualquer servidor voltado para a Internet**, pois eles serão comprometidos. É recomendável usar uma máquina virtual (como [VirtualBox](https://www.virtualbox.org/) ou [VMware](https://www.vmware.com/)), configurada no modo de rede NAT. Dentro da máquina virtual, você pode baixar e instalar o [XAMPP](https://www.apachefriends.org/) para o servidor web e banco de dados.

### ISENÇÃO DE RESPONSABILIDADE

Não nos responsabilizamos pela forma como alguém utiliza esta aplicação (DVWA). Deixamos claro os objetivos da aplicação e não deve ser utilizada maliciosamente. Foram fornecidos avisos e medidas para evitar que os usuários instalem o DVWA em servidores web ativos. Se o seu servidor web for comprometido através da instalação do DVWA, não é de nossa responsabilidade, mas sim da pessoa(s) que o instalou.

- - -

## Licença

Este arquivo faz parte do Damn Vulnerable Web Application (DVWA).

Damn Vulnerable Web Application (DVWA) é um software livre: você pode redistribuí-lo e/ou modificá-lo sob os termos da Licença Pública Geral GNU, publicada pela Free Software Foundation, na versão 3 da Licença ou
(em sua opção) qualquer versão posterior.

Damn Vulnerable Web Application (DVWA) é distribuído na esperança de que seja útil,
mas SEM NENHUMA GARANTIA; sem mesmo a garantia implícita de
COMERCIALIZAÇÃO ou ADEQUAÇÃO A UM PROPÓSITO ESPECÍFICO. Consulte a
Licença Pública Geral GNU para obter mais detalhes.

Você deve ter recebido uma cópia da Licença Pública Geral GNU
junto com o Damn Vulnerable Web Application (DVWA). Se não recebeu, consulte https://www.gnu.org/licenses/.

- - -

## Internationalisation

Este arquivo está disponível em vários idiomas.

- Árabe: [العربية](README.ar.md)
- Chinês: [简体中文](README.zh.md)
- Espanhol: [Español](README.es.md)
- Francês: [Français](README.fr.md)
- Inglês: [English](README.md)
- Persa: [فارسی](README.fa.md)
- Turco: [Türkçe](README.tr.md)

Se você deseja contribuir com uma tradução, por favor envie uma solicitação de pull. No entanto, isso não significa apenas executar a tradução pelo Google Translate e enviar, pois essas serão rejeitadas. Envie a versão traduzida adicionando um novo arquivo 'README.xx.md' onde xx é o código de duas letras do idioma desejado (com base no [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)).

- - -

## Descarga

Enquanto existem várias versões do DVWA disponíveis, a única versão suportada é a última do código-fonte do repositório oficial do GitHub. Você pode cloná-lo do repositório:

```
git clone https://github.com/digininja/DVWA.git
```

Ou [baixe um ZIP dos arquivos](https://github.com/digininja/DVWA/archive/master.zip).

- - -

## Instalação

### Instalação Automatizada 🛠️

**Nota: este não é um script oficial do DVWA, foi escrito por [@IamCarron](https://github.com/IamCarron) e é mantido em [DVWA-Script](https://github.com/IamCarron/DVWA-Script). Muito trabalho foi dedicado à sua criação e verificação, mas recomenda-se inspecionar o script antes de executá-lo no seu sistema. Por favor, reporte qualquer erro no [repositório DVWA-Script](https://github.com/IamCarron/DVWA-Script), não aqui.**

Um script de instalação automatizada para DVWA em sistemas baseados em Debian (incluindo Kali, Ubuntu, Kubuntu, Linux Mint, Zorin OS...). Ele instala automaticamente todas as dependências necessárias, configura o PHP/Apache e inicializa as tabelas do banco de dados prontas para login (`admin` / `password`).

**Nota: Este script requer privilégios de root e é adaptado para sistemas baseados em Debian. Certifique-se de executá-lo como usuário root.**

#### Requisitos de Instalação

- **Sistema Operacional:** Distribuições baseadas em Debian (Kali, Ubuntu, Kubuntu, Linux Mint, Zorin OS, etc.)
- **Privilégios:** Executar como usuário root

#### Passos de Instalação

##### Em uma linha (One-Liner)

Isso fará o download do script de instalação escrito por [@IamCarron](https://github.com/IamCarron) e o executará automaticamente:

```sh
sudo bash -c "$(curl --fail --show-error --silent --location https://raw.githubusercontent.com/IamCarron/DVWA-Script/main/Install-DVWA.sh)"
```

##### Execução manual do script

1. **Baixe o script:**

   ```sh
   wget https://raw.githubusercontent.com/IamCarron/DVWA-Script/main/Install-DVWA.sh
   ```

2. **Torne o script executável:**

   ```sh
   chmod +x Install-DVWA.sh
   ```

3. **Execute como root:**

   ```sh
   sudo ./Install-DVWA.sh
   ```

### Installation Videos

- [Installing DVWA on Kali running in VirtualBox](https://www.youtube.com/watch?v=WkyDxNJkgQ4)
- [Installing DVWA on Windows using XAMPP](https://youtu.be/Yzksa_WjnY0)
- [Installing Damn Vulnerable Web Application (DVWA) on Windows 10](https://www.youtube.com/watch?v=cak2lQvBRAo)

### Windows + XAMPP

The easiest way to install DVWA is to download and install [XAMPP](https://www.apachefriends.org/) if you do not already have a web server setup.

XAMPP is a very easy to install Apache Distribution for Linux, Solaris, Windows and Mac OS X. The package includes the Apache web server, MySQL, PHP, Perl, a FTP server and phpMyAdmin.

This [video](https://youtu.be/Yzksa_WjnY0) walks you through the installation process for Windows but it should be similar for other OSs.

### Arquivo de configuração

DVWA vem com uma cópia fictícia do seu arquivo de configuração que você precisa copiar para o local correto e fazer as alterações apropriadas. No Linux, supondo que você esteja no diretório do DVWA, isso pode ser feito da seguinte forma:

`cp config/config.inc.php.dist config/config.inc.php`

No Windows, isso pode ser um pouco mais difícil se você estiver ocultando as extensões de arquivo. Se você não tem certeza disso, este post de blog explica mais sobre o assunto:

[How to Make Windows Show File Extensions](https://www.howtogeek.com/205086/beginner-how-to-make-windows-show-file-extensions/)

### Linux Packages

Se você estiver usando uma distribuição Linux baseada em Debian, será necessário instalar os seguintes pacotes (ou seus equivalentes):

- apache2
- libapache2-mod-php
- mariadb-server
- mariadb-client
- php php-mysqli
- php-gd

É recomendado fazer uma atualização antes disso para garantir que você vai obter a versão mais recente de tudo

```
apt update
apt install -y apache2 mariadb-server mariadb-client php php-mysqli php-gd libapache2-mod-php
```

Embora o site possa funcionar com MySQL, recomendamos fortemente o uso do MariaDB, já que ele é compatível sem necessidade de ajustes adicionaisr.

### Configuração do Banco de Dados

Para configurar o banco de dados, basta clicar no botão `Setup DVWA` no menu principal e, em seguida, clicar no botão `Create / Reset Database`. Isso irá criar/reconfigurar o banco de dados para você com alguns dados.

Se você receber um erro ao tentar criar seu banco de dados, verifique se suas credenciais do banco de dados estão corretas dentro de `./config/config.inc.php`. *Isso difere do config.inc.php.dist, que é um arquivo de exemplo.*

Por padrão, as variáveis são definidas da seguinte maneira:

```php
$_DVWA[ 'db_server'] = '127.0.0.1';
$_DVWA[ 'db_port'] = '3306';$_DVWA[ 'db_user' ] = 'dvwa';
$_DVWA[ 'db_password' ] = 'p@ssw0rd';
$_DVWA[ 'db_database' ] = 'dvwa';
```

Observação: se você estiver usando o MariaDB em vez do MySQL (o MariaDB é o padrão no Kali), você não pode usar o usuário root do banco de dados, você deve criar um novo usuário de banco de dados. Para fazer isso, conecte-se ao banco de dados como usuário root e use os seguintes comandos:

```mysql
mysql> create database dvwa;
Query OK, 1 row affected (0.00 sec)

mysql> create user dvwa@localhost identified by 'p@ssw0rd';
Query OK, 0 rows affected (0.01 sec)

mysql> grant all on dvwa.* to dvwa@localhost;
Query OK, 0 rows affected (0.01 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```

### Desabilitar autenticação

Alguns ferramentas não funcionam bem com autenticação e não podem ser usadas com o DVWA. Para contornar isso, há uma opção de configuração para desativar a verificação de autenticação. Para fazer isso, basta definir o seguinte no arquivo de configuração:

```php
$_DVWA[ 'disable_authentication' ] = true;
```

Você também precisará definir o nível de segurança que seja apropriado para os testes que deseja realizar:

```php
$_DVWA[ 'default_security_level' ] = 'low';
```
Nesse estado, você pode acessar todos os recursos sem precisar fazer login ou definir cookies.

### Outra configuração

Dependendo do seu sistema operacional, assim como a versão do PHP, você pode desejar alterar a configuração padrão. A localização dos arquivos será diferente em cada máquina.

**Permissões de diretório**:

* `./hackable/uploads/` - Precisa estar com permissão de escrita pelo serviço web (para envio de arquivos).
* `./external/phpids/0.6/lib/IDS/tmp/phpids_log.txt` - Precisa estar gravável pelo serviço web (se você deseja usar o PHPIDS).

**PHP configuration**:
* Para permitir Inclusões de Arquivos Remotos (RFI):
    * `allow_url_include = on` [[allow_url_include](https://secure.php.net/manual/en/filesystem.configuration.php#ini.allow-url-include)]
    * `allow_url_fopen = on` [[allow_url_fopen](https://secure.php.net/manual/en/filesystem.configuration.php#ini.allow-url-fopen)]
* Para reduzir opcionalmente a verbosidade ocultando mensagens de aviso do PHP:
    * `display_errors = off` [[display_errors](https://secure.php.net/manual/en/errorfunc.configuration.php#ini.display-errors)]

**Arquivo: `config/config.inc.php`**:

* `$_DVWA[ 'recaptcha_public_key' ]` & `$_DVWA[ 'recaptcha_private_key' ]` - Esses valores precisam ser gerados em: https://www.google.com/recaptcha/admin/create

### Credenciais Padrão

**Default username = `admin`**

**Default password = `password`**

_...Podem ser facilmente bruteforceados ;)_

Login URL: http://127.0.0.1/login.php

_Nota: Isso será diferente se você instalou o DVWA em um diretório diferente._

- - -

## Docker Container

_Esta seção do readme foi adicionada por @thegrims, para suporte com Docker, por favor entre em contato com ele ou @opsxcq que é o mantenedor da imagem e repositório Docker. Qualquer ticket de problema provavelmente será encaminhado para eles e fechado._

- [dockerhub site](https://hub.docker.com/r/vulnerables/web-dvwa/)
`docker run --rm -it -p 80:80 vulnerables/web-dvwa`

Por favor, certifique-se de que está usando aufs devido a problemas anteriores do MySQL. Execute `docker info` para verificar seu driver de armazenamento. Se não for aufs, altere-o como tal. Existem guias para cada sistema operacional sobre como fazer isso, mas são bastante diferentes, então não abordaremos isso aqui.

- - -

## Troubleshooting

Estes pressupõem que você está em uma distribuição baseada em Debian, como Debian, Ubuntu e Kali. Para outras distribuições, siga o tutorial, mas atualize o comando, se necessário.

### Acessei o site e obtive um erro 404

Se você está tendo esse problema, precisa entender as localizações dos arquivos. Por padrão, a raiz do documento Apache (o local onde ele começa a procurar conteúdo da web) é `/var/www/html`. Se você colocar o arquivo `hello.txt` neste diretório, para acessá-lo, você deve navegar para `http://localhost/hello.txt`.

Se você criou um diretório e colocou o arquivo lá - `/var/www/html/mydir/hello.txt` - você precisará navegar para `http://localhost/mydir/hello.txt`.

O Linux é sensível a maiúsculas e minúsculas por padrão e, portanto, no exemplo acima, se você tentasse navegar em qualquer um desses endereços, receberia um erro `404 Not Found`:

- `http://localhost/MyDir/hello.txt`
- `http://localhost/mydir/Hello.txt`
- `http://localhost/MYDIR/hello.txt`

Como isso afeta o DVWA? A maioria das pessoas usa o Git para baixar o DVWA em `/var/www/html`, o que lhes dá o diretório `/var/www/html/DVWA/` com todos os arquivos do DVWA dentro dele. Então, eles navegam até `http://localhost/` e recebem um `404` ou a página de boas-vindas padrão do Apache. Como os arquivos estão em DVWA, você deve navegar para `http://localhost/DVWA`.

O outro erro comum é navegar para `http://localhost/dvwa`, o que resultará em um erro `404` porque `dvwa` não é o mesmo que `DVWA` em termos de correspondência de diretório no Linux.

Portanto, após a instalação, se você tentar visitar o site e receber um erro `404`, pense em onde instalou os arquivos, em relação à raiz do documento, e qual é a caixa (alta ou baixa).

### "Acess denied" ao executar a configuração

Se você vir o seguinte ao executar o script de configuração, significa que o nome de usuário ou a senha no arquivo de configuração não correspondem aos configurados no banco de dados:

```
Database Error #1045: Access denied for user 'notdvwa'@'localhost' (usando a senha "YES").
```

O erro está dizendo que você está usando o nome de usuário `notdvwa`.

O seguinte erro indica que você apontou o arquivo de configuração para o banco de dados errado.

```
SQL: Access denied for user 'dvwa'@'localhost' to database 'notdvwa'
```

Está dizendo que você está usando o usuário `dvwa` e tentando se conectar ao banco de dados `notdvwa`.

A primeira coisa a fazer é verificar se o que você acha que colocou no arquivo de configuração é realmente o que está lá.

Se corresponder ao que você espera, a próxima coisa a fazer é verificar se você pode fazer login como usuário no terminal. Supondo que você tenha um usuário de banco de dados chamado dvwa e uma senha de p@ssw0rd, execute o seguinte comando:

```
mysql -u dvwa -pp@ssw0rd -D dvwa
```
Nota: Não há espaço após o -p

Se você vir o seguinte, a senha está correta:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 14
Server version: 10.3.22-MariaDB-0ubuntu0.19.10.1 Ubuntu 19.10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [dvwa]>
```

Como você conseguiu conectar no terminal, provavelmente algo está errado no arquivo de configuração. Verifique novamente o arquivo e se ainda assim não conseguir resolver, abra um issue.

Se você receber a seguinte mensagem, significa que o nome de usuário ou a senha que você está usando estão incorretos. Repita as etapas da [Configuração do Banco de Dados](#database-setup) e certifique-se de usar o mesmo nome de usuário e senha em todo o processo.

```
ERROR 1045 (28000): Access denied for user 'dvwa'@'localhost' (usando a senha: YES)
```

Se você obtiver o seguinte erro, as credenciais do usuário estão corretas, mas o usuário não tem acesso ao banco de dados. Novamente, repita as etapas de configuração e verifique o nome do banco de dados que você está usando.

```
ERROR 1044 (42000): Access denied for user 'dvwa'@'localhost' to database 'dvwa'
```
O erro final que você pode receber é este:

```
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
```

Este não é um problema de autenticação, mas indica que o servidor de banco de dados não está em execução. Inicie-o com o seguinte comando:

```sh
sudo service mysql start
```

### Unknown authentication method

Com as versões mais recentes do MySQL, o PHP não pode mais se comunicar com o banco de dados em sua configuração padrão. Se você tentar executar o script de configuração e receber a seguinte mensagem, significa que há uma configuração incorreta.

```
Database Error #2054: The server requested authentication method unknown to the client.
```

Você tem duas opções, a mais fácil é desinstalar o MySQL e instalar o MariaDB. O seguinte é o guia oficial do projeto MariaDB:

<https://mariadb.com/resources/blog/how-to-migrate-from-mysql-to-mariadb-on-linux-in-five-steps/>

Alternativamente, siga estes passos:

1. Como root, edite o seguinte arquivo: `/etc/mysql/mysql.conf.d/mysqld.cnf`
2. Abaixo da linha `[mysqld]`, adicione o seguinte:
  `default-authentication-plugin=mysql_native_password`
3. Reinicie o banco de dados: `sudo service mysql restart`
4. Verifique o método de autenticação para o usuário do seu banco de dados:

    ```sql
    mysql> select Host,User, plugin from mysql.user where mysql.user.User = 'dvwa';
    +-----------+------------------+-----------------------+
    | Host      | User             | plugin                |
    +-----------+------------------+-----------------------+
    | localhost | dvwa             | caching_sha2_password |
    +-----------+------------------+-----------------------+
    1 rows in set (0.00 sec)
    ```

5. Provavelmente você verá `caching_sha2_password`. Se for esse o caso, execute o seguinte comando:

    ```sql
    mysql> ALTER USER dvwa@localhost IDENTIFIED WITH mysql_native_password BY 'p@ssw0rd';
    ```

6. Executando novamente a verificação, agora você deve ver `mysql_native_password`.

    ```sql
    mysql> select Host,User, plugin from mysql.user where mysql.user.User = 'dvwa';
    +-----------+------+-----------------------+
    | Host      | User | plugin                |
    +-----------+------+-----------------------+
    | localhost | dvwa | mysql_native_password |
    +-----------+------+-----------------------+
    1 row in set (0.00 sec)
    ```

Após tudo isso, o processo de configuração deve funcionar normalmente.

Se você quiser mais informações, consulte a seguinte página: https://www.php.net/manual/en/mysqli.requirements.php.

### Database Error #2002: No such file or directory.

O servidor de banco de dados não está em execução. Em uma distribuição baseada em Debian, isso pode ser feito com o seguinte comando:

```sh
sudo service mysql start
```

### Erros "MySQL server has gone away" and "Packets out of order"

Existem algumas razões pelas quais você pode estar recebendo esses erros, mas a mais provável é que a versão do servidor de banco de dados que você está executando não seja compatível com a versão do PHP.

Isso é mais comumente encontrado quando você está executando a versão mais recente do MySQL, pois o PHP e o MySQL não se dão bem. O melhor conselho é abandonar o MySQL e instalar o MariaDB, já que isso não é algo que possamos oferecer suporte.

Para mais informações, consulte:

<https://www.ryadel.com/en/fix-mysql-server-gone-away-packets-order-similar-mysql-related-errors/>

### Injeção de comando não funciona

O Apache pode não ter privilégios suficientes para executar comandos no servidor web. Se você estiver executando o DVWA no Linux, certifique-se de estar logado como root. No Windows, faça login como Administrador.

### Por que o banco de dados não pode se conectar no CentOS?

Você pode estar tendo problemas com o SELinux. Desative o SELinux ou execute este comando para permitir que o servidor web se comunique com o banco de dados:
```
setsebool -P httpd_can_network_connect_db 1
```

### Mais Alguma Coisa

Para obter as informações mais recentes de solução de problemas, leia os tickets abertos e fechados no repositório do git:

<https://github.com/digininja/DVWA/issues>

Antes de enviar um ticket, certifique-se de que está executando a versão mais recente do código do repositório. Esta não é a última versão lançada, mas sim o último código da master branch.

Se você estiver abrindo um chamado de suporte, por favor, forneça pelo menos as seguintes informações:

- Sistema operacional
- As últimas 5 linhas do log de erro do servidor web logo após o erro que está relatando
- Se for um problema de autenticação do banco de dados, siga os passos acima e tire uma captura de tela de cada etapa. Envie essas informações juntamente com uma captura de tela da seção do arquivo de configuração que mostra o usuário e a senha do banco de dados.
- Uma descrição completa do que está acontecendo, o que você espera que aconteça e o que tentou fazer para resolver o problema. "login broken" não é suficiente para entendermos o seu problema e ajudá-lo a corrigi-lo.

- - -

## Tutoriais

Vou tentar criar alguns vídeos tutoriais que expliquem algumas das vulnerabilidades e mostrem como detectá-las e explorá-las. Aqui estão os que eu fiz até agora:

[Finding and Exploiting Reflected XSS](https://youtu.be/V4MATqtdxss)

- - -

## SQLite3 SQL Injection

_O suporte para isso é limitado, antes de levantar problemas, por favor, certifique-se de estar preparado para depurar, não simplesmente alegue "não funciona"._

Por padrão, o SQLi e o Blind SQLi são feitos contra o servidor MariaDB/MySQL usado pelo site, mas é possível alternar para fazer os testes SQLi contra o SQLite3.

Eu não vou cobrir como fazer o SQLite3 funcionar com o PHP, mas deve ser um caso simples de instalar o pacote `php-sqlite3` e garantir que ele esteja habilitado.

Para fazer a mudança, simplesmente edite o arquivo de configuração e adicione ou edite estas linhas:

```
$_DVWA["SQLI_DB"] = "sqlite";
$_DVWA["SQLITE_DB"] = "sqli.db";
```

Por padrão, ele usa o arquivo `database/sqli.db`, se você bagunçar, basta copiar `database/sqli.db.dist` por cima.

Os desafios são exatamente os mesmos do MySQL, mas são executados no SQLite3 em vez disso.

- - -

👨‍💻 Contribudores
-----

Obrigado por todas as suas contribuições e por manter este projeto atualizado. :heart:

Se você tiver alguma ideia, alguma melhoria ou simplesmente quiser colaborar, você é bem-vindo a contribuir e participar do projeto, sinta-se à vontade para enviar sua PR.

<p align="center">
<a href="https://github.com/digininja/DVWA/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=digininja/DVWA&max=500">
</a>
</p>

- - -

## Links

Project Home: <https://github.com/digininja/DVWA>

*Created by the DVWA team*

