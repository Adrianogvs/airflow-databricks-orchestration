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
2. No canto superior direito, clique em **Settings**.

4. Vá para `User Settings → Developer → Access Tokens`.
5. Clique em **Generate New Token**.
6. Adicione uma descrição (ex: `Airflow Integration`) e defina um tempo de expiração.
7. Clique em **Generate** e **copie o token** (ele não será exibido novamente).
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

---

## 🧩 Passo 3: Configurar a Conexão do Airflow com o Databricks

1. Acesse a interface do Airflow (ex: `http://localhost:8080`).

2. Vá em **Admin → Connections**.

3. Clique em **+ (Adicionar Nova Conexão)**.

4. Preencha os campos:

   * **Connection Id**: `databricks_default` (ou um nome personalizado).
   * **Connection Type**: `Databricks`.
   * **Host**: URL do seu workspace Databricks (ex: `https://<seu-workspace>.cloud.databricks.com`).
   * **Password**: Cole o PAT (Token de Acesso) gerado no Passo 1.

5. Clique em **Save**.

---

## 🧩 Passo 4: Criar um DAG no Airflow para Disparar Jobs no Databricks

1. Vá para a pasta `dags/` no diretório de instalação do Airflow.
2. Crie um novo arquivo Python (ex: `databricks_job_trigger.py`).
3. Use o seguinte código como base:

```python
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'databricks_job_trigger',
    default_args=default_args,
    schedule_interval=None,  # Pode ser definido (ex: '@daily')
    catchup=False,
) as dag:

    submit_job = DatabricksSubmitRunOperator(
        task_id='submit_databricks_job',
        databricks_conn_id='databricks_default',  # Nome da conexão criada
        existing_cluster_id='<ID_DO_CLUSTER>',  # Ou use `new_cluster` para criar um novo
        notebook_task={
            'notebook_path': '/caminho/do/seu/notebook',
        },
        # Alternativamente, use `spark_python_task` ou `spark_jar_task`
    )

    submit_job
```

### Onde obter os parâmetros?

* `existing_cluster_id`: Encontre no Databricks em **Clusters → Selecione o cluster → Configuration**.
* `notebook_path`: Caminho do notebook no Databricks (ex: `/Users/seu_usuario/meu_notebook`).

---

## 🧩 Passo 5: Testar e Executar o DAG

1. Salve o arquivo na pasta `dags/`.
2. No painel do Airflow, atualize a lista de DAGs.
3. Localize o DAG `databricks_job_trigger` e ative-o.
4. Execute manualmente clicando em **Trigger DAG**.
5. Verifique o status no Databricks (Jobs → Runs).

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


[def]: D:\Documents\GitHub\project-with-airflow-docker\img\01.png
