Reporting API — Quick Gist and How It Influences Our Architecture

Summary (from scanning reporting-api)
- Tech stack: Kotlin + Micronaut modules (api, core, data-provider, db, gateway). Uses jOOQ-generated code for DB (PostgreSQL), Micronaut DI, OpenAPI, and Helm/Docker for deployment.
- Batch/ETL style: There are batch processors that paginate through source data and compute metrics per workspace/community/date.
  - Example: api/src/main/kotlin/com/ideascale/reporting/task/processor/IdeaStatProcessor.kt
    - fetchDailyData(): iterates workspaces, computes daily stats for Idea activity types.
    - reset(): clears and recomputes stats from a start date.
    - Uses ReportingDataProvider to read data (findWorkspaceIds, findCommunityIds, getIdeaStatistics, etc.).
    - Writes aggregated stats via IdeaStatisticsService.
  - ProcessorBase coordinates paging, workspace selection, and date ranges.
- DB module (db): configures schema = "reporting" and generates jOOQ classes; packaged into a migration Docker image.
- Gateway/core modules: shared contracts, mapping, Micronaut setup, and OpenAPI publication.

Implications for Python rewrite
- Fit: Reporting is a classic candidate for background processing and eventual separate service due to its batch nature and distinct scaling profile.
- Modular Monolith approach (now):
  - Implement reporting as a background worker within the monolith (Celery/Dramatiq/RQ) using the same DB.
  - Mirror patterns:
    - Data provider port (queries across workspace/community/idea activities).
    - Service for writing aggregated metrics tables.
    - Processors for daily and reset re-computation.
  - Use the Outbox pattern to emit events (IdeaCreated, StageChanged, etc.) to incrementally maintain aggregates in near real-time if needed.
- Microservice extraction (later):
  - Reporting can be split into a dedicated service with its own read store (reporting schema) fed by events from the core.
  - Keep interfaces clean: define reporting API for dashboards and exports.
  - Scale workers independently; optionally use Kafka/NATS for ingestion.

Recommendations
- Short term: build reporting processors as jobs in the monolith’s worker; define clear ports for data input/output and write tests with table-driven cases.
- Medium term: if compute or latency demands grow, extract reporting into a service; reuse the same event contracts and migrate data-provider to event-driven ingestion.

Cross-references
- ADR-001-Architecture-Style-Microservices-vs-Modular-Monolith.md — decision and EDA guidance.
- PYTHON_REWRITE_PLAN.md — background workers, policy engine, and events strategy.
