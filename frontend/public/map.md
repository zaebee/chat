# Архитектурные диаграммы Hive

## 1. Общая схема (`docs/01_ARCHITECTURE/OVERVIEW.md`)

```mermaid
graph TD
    subgraph "Hive Architectural Blueprint"
        subgraph "Core ATCG Pillars"
            A[Aggregate<br/>Data Structuring]
            T[Transformation<br/>Data Processing]
            C[Connector<br/>Communication]
            G[Genesis<br/>System Initialization]
        end

        subgraph "Cross-Cutting Concerns"
            SEC[Security<br/>Pervasive Protection]
            MET[Metrics & Observability<br/>System Monitoring]
            LOG[Logging & Auditing<br/>Event Tracking]
            CONF[Configuration<br/>System Parameters]
        end

        subgraph "Data Flow & Protocols"
            POLLEN[Pollen Protocol<br/>Standardized Events]
            WS[WebSocket<br/>Real-time Stream]
            API[Internal APIs<br/>Component Interaction]
        end

        subgraph "Review & Development Process"
            BEE_PEER[Bee-to-Peer Methodology<br/>Human Review]
            ASSIST[Review Assistant Tools<br/>Automated Aids]
            PR_TEMP[PR Templates<br/>Contribution Guides]
        end
    end

    %% Core ATCG Interactions
    A -- Data --> T
    T -- Transformed Data --> C
    C -- Messages --> G
    G -- System Events --> A

    %% Cross-Cutting Application
    SEC -- Protects --> A & T & C & G
    MET -- Monitors --> A & T & C & G
    LOG -- Records --> A & T & C & G
    CONF -- Configures --> A & T & C & G

    %% Data Flow Usage
    C -- Uses --> POLLEN & WS & API
    POLLEN -- Carries --> Data
    WS -- Transmits --> Messages
    API -- Defines --> Interactions

    %% Review Process Interaction
    BEE_PEER -- Guides --> ASSIST
    ASSIST -- Uses --> PR_TEMP
    ASSIST -- Analyzes --> A & T & C & G
```

2. Диаграмма компонента Connector

docs/01_ARCHITECTURE/COMPONENTS/CONNECTOR.md

```mermaid
flowchart TD
    subgraph "Connector (C) Component: Communication Flow"
        INPUT["External Input<br/>(e.g., WebSocket Message)"] --> VALIDATE["Input Validation<br/>(SecurityHardening)"]
        VALIDATE -- Valid --> PROTOCOL_TRANSLATE["Protocol Translation<br/>(ChatProtocolTranslator)"]
        PROTOCOL_TRANSLATE -- Pollen Event --> EVENT_BUS["Hive Event Bus<br/>(HiveEventBridge)"]
        EVENT_BUS -- Publish/Subscribe --> INTERNAL_COMPONENTS[Internal Hive Components]

        VALIDATE -- Invalid --> ERROR_HANDLER["Error Handling<br/>(Security Violation)"]
        ERROR_HANDLER --> LOG[Log Error]

        INTERNAL_COMPONENTS -- Response --> EVENT_BUS
        EVENT_BUS -- Pollen Event --> PROTOCOL_TRANSLATE
        PROTOCOL_TRANSLATE -- Translated --> OUTPUT["External Output<br/>(e.g., WebSocket Message)"]
    end
```

3. Структуры данных

docs/01_ARCHITECTURE/DATA_STRUCTURES/POLLEN_EVENT.md

```mermaid
classDiagram
    class PollenEvent {
        +string event_id
        +string event_type
        +string version
        +string timestamp
        +string aggregate_id
        +Record<string, unknown> payload
        +string source_component
        +string correlation_id
        +string[] tags
    }

    class ConnectorMessage {
        +string id
        +string messageType
        +Record<string, unknown> payload
        +number priority
        +string timestamp
        +string sourceId
        +string targetId
    }

    PollenEvent <|-- ConnectorMessage : translates
```