# MEDSURE System Architecture (Mermaid)\n\n```mermaid\n%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#0F172A',
    'primaryTextColor': '#F8FAFC',
    'primaryBorderColor': '#38BDF8',
    'lineColor': '#0284C7',
    'secondaryColor': '#F0FDFA',
    'tertiaryColor': '#F8FAFC',
    'fontFamily': 'Inter, system-ui, sans-serif',
    'fontSize': '13px'
}}}%%

flowchart TB
    %% Users & Channels
    subgraph Clients ["  CLIENT LAYER (PATIENT & ADVOCATE TOUCHPOINTS)  "]
        direction LR
        User(["👤 Patient / Caregiver / Insurance Advocate"]):::userStyle
        Browser(["🌐 Responsive Web Browser (Desktop / Mobile)"]):::clientStyle
        User --> Browser
    end

    %% Frontend App
    subgraph Frontend ["  FRONTEND ARCHITECTURE (Next.js 14 App Router)  "]
        direction TB
        Landing["🏠 Landing & Dual-Act Overview<br/><code>/</code>"]:::feStyle
        Dash["📊 Live Real-Time Dashboard<br/><code>/dashboard</code>"]:::feStyle
        
        subgraph Act1FE ["Act 1: Pre-Admission"]
            Triage["🔍 Fair Price Estimator<br/><code>/triage</code><br/><i>(Hindi & English NLP + Red Flags)</i>"]:::feStyle
            Charts["📈 Interactive Price Bounds<br/><i>Recharts Min / Median / Cap</i>"]:::feStyle
            Triage --> Charts
        end

        subgraph Act2FE ["Act 2: Post-Discharge"]
            Upload["📄 Bill Upload Ingestion<br/><code>/bills/upload</code>"]:::feStyle
            Review["✏️ Human-in-the-Loop Review<br/><code>/bills/[id]/review</code>"]:::feStyle
            AuditView["🚨 Findings & Proofs<br/><code>/audits/[id]</code>"]:::feStyle
            DisputeView["✉️ Dispute Letter Modal<br/><code>/audits/[id]/dispute-letter</code>"]:::feStyle
            Upload --> Review --> AuditView --> DisputeView
        end

        RefRates["📚 Official Tariffs<br/><code>/reference-rates</code>"]:::feStyle
    end

    Browser --> Landing
    Browser --> Dash
    Browser --> Triage
    Browser --> Upload
    Browser --> RefRates

    %% API Gateway Layer
    subgraph Gateway ["  FASTAPI ASGI GATEWAY (Python 3.12 / 3.14 + Uvicorn)  "]
        direction LR
        APIRouter["⚡ REST API Router (<code>/api/v1</code>)<br/><i>JWT Auth • Pydantic v2 • Swagger Docs</i>"]:::gwStyle
    end

    Charts -.->|POST /api/v1/estimates| APIRouter
    Upload -.->|POST /api/v1/bills/upload| APIRouter
    Review -.->|PATCH /api/v1/bills/[id]/line-items| APIRouter
    AuditView -.->|POST /api/v1/bills/[id]/audit| APIRouter
    DisputeView -.->|GET /api/v1/audits/[id]/dispute-letter| APIRouter
    RefRates -.->|GET /api/v1/reference-rates| APIRouter
    Dash -.->|GET /api/v1/dashboard/summary| APIRouter

    %% Backend Services Layer
    subgraph Backend ["  BACKEND SERVICES ENGINE  "]
        direction TB

        subgraph SvcAct1 ["Act 1 Services"]
            TriageSvc["🩺 Triage & Safety Service<br/>• Bilingual Tokenizer (Hindi/English)<br/>• Emergency Red-Flag Shield (112/108)"]:::svcStyle
            EstimatorSvc["💰 Cost Estimator Engine<br/>• Procedural Code Mapping<br/>• Deterministic Tariff Bounds Calculator"]:::svcStyle
            TriageSvc --> EstimatorSvc
        end

        subgraph SvcAct2 ["Act 2 Services"]
            OCRSvc["👁️ Document Ingestion & OCR<br/>• PyMuPDF (fitz) Native PDF Vector<br/>• Pillow + Tesseract Vision Fallback"]:::svcStyle
            NormalizerSvc["🧹 Bill Normalizer<br/>• Token Confidence Scoring<br/>• Tabular Line-Item Extractor"]:::svcStyle
            
            AuditEngine["⚖️ Deterministic Audit Engine<br/><b>Pure Python Decimal Arithmetic (Zero Hallucination)</b><br/>• Rule A: Math & Multiplication (Qty × Rate ≠ Total)<br/>• Rule B: Duplicate Procedural Fees (Duplicate OT)<br/>• Rule C: Reference Tariff Cap Violations (NPPA/CGHS)<br/>• Rule D: Unbundling Consumables on Packages<br/>• Rule E: Incomplete / Missing Tariff Data"]:::auditStyle
            
            ReportSvc["📑 Report & Dispute Generator<br/>• ReportLab Signed PDF Generator<br/>• Statutory Hospital Dispute Drafter"]:::svcStyle

            OCRSvc --> NormalizerSvc --> AuditEngine --> ReportSvc
        end
    end

    APIRouter --> TriageSvc
    APIRouter --> OCRSvc
    APIRouter --> AuditEngine
    APIRouter --> ReportSvc

    %% Data & Storage Layer
    subgraph Storage ["  PERSISTENCE & ARTIFACT REPOSITORY  "]
        direction LR
        SQLDB[("🗄️ Relational Database<br/><i>SQLAlchemy 2.0 ORM</i><br/>• SQLite (Dev Zero-Friction)<br/>• PostgreSQL (Prod Ready)")]:::dbStyle
        UploadsVault[("📁 Encrypted File Vault<br/><code>/uploads</code><br/><i>Raw Invoices & SHA-256 Hashes</i>")]:::dbStyle
        ReportsVault[("📜 Artifacts Repository<br/><code>/generated_reports</code><br/><i>Signed Verification PDFs</i>")]:::dbStyle
    end

    EstimatorSvc <-->|Query Benchmark Caps| SQLDB
    AuditEngine <-->|Verify Against Tariffs| SQLDB
    OCRSvc -->|Store Original| UploadsVault
    ReportSvc -->|Save PDF| ReportsVault

    %% External Benchmarks
    subgraph ExtBenchmarks ["  EXTERNAL STATUTORY BENCHMARKS  "]
        direction TB
        CGHS["🏛️ Central Govt Health Scheme (CGHS Rates)"]:::extStyle
        NPPA["⚖️ NPPA Price Ceilings (Stents & Implants)"]:::extStyle
        ROHINI["🏥 Registry of Hospitals in Network of Insurers"]:::extStyle
    end

    ExtBenchmarks -.->|Seeded / Versioned Tariffs| SQLDB

    %% Custom Styling Classes
    classDef userStyle fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC,font-weight:bold;
    classDef clientStyle fill:#1E293B,stroke:#94A3B8,stroke-width:1px,color:#F1F5F9;
    classDef feStyle fill:#F0FDF4,stroke:#16A34A,stroke-width:1.5px,color:#14532D,font-weight:500;
    classDef gwStyle fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef svcStyle fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#1E3A8A;
    classDef auditStyle fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#7F1D1D,font-weight:bold;
    classDef dbStyle fill:#F8FAFC,stroke:#475569,stroke-width:1.5px,color:#0F172A;
    classDef extStyle fill:#FAF5FF,stroke:#9333EA,stroke-width:1px,color:#581C87;\n```\n