# Airflow

[Back](../../index.md)

- [Airflow](#airflow)
  - [Install](#install)
  - [Core Components](#core-components)
  - [Core concept](#core-concept)
  - [Architecture 架构](#architecture-架构)

## Install

- Install Docker

## Core Components

- Web server(flask)
- Scheduler
- Metastore
  - a db store metadata
- Triggerer
- Executor: 并不实际执行, 而是定义如何和哪个系统进程执行. 工作实际上是在 proecess 执行.
  - queue:定义task的顺序
  - worker: 实际执行任我

## Core concept

- DAG:
  - 架构, 单向依赖,
- Operator:
  - action operator: execute sth
  - transfer operator: transfer data from A to B
  - sensor operator: wait for sth to happen
- Task/Task instance:
  - an operator is a task
  - an operator needs a task instance
- Workflow:
  - 工作流

---

## Architecture 架构

- One node 架构
- multi nodes
