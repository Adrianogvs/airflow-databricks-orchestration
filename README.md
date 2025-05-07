# Manual Passo a Passo: Configuração do Airflow para Orquestrar Jobs no Databricks

Este manual explica como configurar o Apache Airflow para orquestrar jobs no Databricks.

---

## ✅ Pré-requisitos

* Ambiente Airflow configurado e em execução.
* Acesso a um workspace do Databricks (Azure Databricks, AWS Databricks, etc.).
* Permissões para gerar tokens de acesso (PAT - Personal Access Token) no Databricks.

---

## 🧩 Passo 1: Gerar um Token de Acesso (PAT) no Databricks

1. Acesse o Databricks Workspace.
2. No canto superior direito, clique em **Settings**.<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/01.png)

4. Vá para `User Settings → Developer → Access Tokens`.<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/02.png)

5. Clique em **Generate New Token**.<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/03.png)

6. Adicione uma descrição (ex: `Airflow Integration`) e defina um tempo de expiração.

7. Clique em **Generate** e **copie o token** (ele não será exibido novamente).<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/04.png)

8. Salve o token em um local seguro (será usado no Airflow).

---

## 🧩 Passo 2: Instalar o Provedor de Conexão do Databricks no Airflow

O Airflow requer um pacote adicional para se conectar ao Databricks.

No terminal do servidor onde o Airflow está instalado, execute:

```bash
pip install apache-airflow-providers-databricks
```

Após a instalação, reinicie os serviços do Airflow:

```bash
airflow webserver --stop  
airflow scheduler --stop  
airflow webserver --start  
airflow scheduler --start  
```
### Passo alternativo - Instalação do Provedor de Conexão do Databricks no Airflow

1. Configure os containers no Docker. Ajuste os três objetos conforme a imagem abaixo:<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/05.png)

2. Clique nos tres pontinhos e selecione a opção **Open in terminal**. <br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/06.png)

3. Irá abrir o terminal do Docker, cole o código ```ip install apache-airflow-providers-databricks``` e logo após pressione **Enter**.<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/08.png)

4. Repita o processo para os demais containers.<br>
   II. airflow-worker-1<br>
   III. airflow-scheduler-1
---

## 🧩 Passo 3: Configurar a Conexão do Airflow com o Databricks

1. Acesse a interface do Airflow (ex: `http://localhost:8080`).

2. Vá em **Admin → Connections**.<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/10.png)

3. Clique em **+ (Adicionar Nova Conexão)**.<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/11.png)

4. Preencha os campos:

   * **Connection Id**: `databricks_default` (ou um nome personalizado).
   * **Connection Type**: `Databricks`.
   * **Host**: URL do seu workspace Databricks (ex: `https://<seu-workspace>.cloud.databricks.com`).
   * **Password**: Cole o PAT (Token de Acesso) gerado no Passo 1.<br>
   
    ![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/14.png)

5. Clique em **Save**.

---

## 🧩 Passo 4: Criar um DAG no Airflow para Disparar Jobs no Databricks

1. Vá para a pasta `dags/` no diretório de instalação do Airflow.
2. Crie um novo arquivo Python (ex: `databricks_dag.py`).
3. Use o seguinte código como base:

```python
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow'
}

with DAG('databricks_dag',
    start_date = days_ago(2),
    schedule_interval = None,
    default_args = default_args
) as dag:
    
    opr_run_now = DatabricksRunNowOperator(
        task_id = 'run_now',
        databricks_conn_id = 'databricks', # Nome do Conn Id da List Connection
        job_id = <ID_TOKENS_ACCESS> # Access tokens gerado no Databricks 
    )

```

---

## 🧩 Passo 5: Testar e Executar o DAG

1. Salve o arquivo na pasta `dags/`.
2. No painel do Airflow, atualize a lista de DAGs.
3. Localize o DAG `ddatabricks_dag` e ative-o.
4. Execute manualmente clicando em **Trigger DAG**.
5. Verifique o status no Databricks (Jobs → Runs).<br>
![](https://github.com/Adrianogvs/airflow-databricks-orchestration/blob/main/img/15.png)

---

## 📅 Configuração Avançada

### Agendamento Automático

Modifique o `schedule_interval` no DAG para disparar automaticamente:

* `@daily` → Todos os dias.
* `0 0 * * 0` → Todo domingo à meia-noite (cron syntax).

### Parâmetros Dinâmicos

Use `{{ ds }}` (data de execução) ou variáveis do Airflow para passar parâmetros ao notebook.

---

## ⚠️ Solução de Problemas

* **Erro "Databricks connection type not found"**: Verifique se o provider foi instalado corretamente e reinicie o Airflow.
* **Falha na autenticação**: Confira se o PAT está correto e não expirou.
* **Cluster indisponível**: Verifique se o cluster está ativo no Databricks.

---

## 🚀 Conclusão

Agora o Airflow está configurado para orquestrar jobs no Databricks, seja manualmente ou de forma agendada.

> 📌 **Dica**: Sempre revogue tokens não utilizados no Databricks por segurança.

> 🔗 **Referência**: Documentação do Airflow-Databricks

### Próximos passos:

* Automatizar pipelines mais complexos com múltiplos jobs.
* Usar Databricks Jobs API para maior controle.
* Configurar alertas de falhas no Airflow.

Espero que este manual seja útil! 🚀
