# Database Directory

## 1. Purpose
This folder details the database structures, relational schemas, and indexing strategies used to store telemetry and incident metadata.

---

## 2. Future Contents
- `migrations/`: SQL migration files defining table constraints.
- `schemas/`: Conceptual ERD files and database configuration variables.
- `seeding/`: Mock data parameters to seed databases during testing phases.

---

## 3. Responsible Member
- **Primary Owner**: Researcher 2 (Cloud & Database Architect)

---

## 4. Expected Deliverables
- Normalized SQL schemas for drones, telemetry histories, and logged incidents.
- Indexes on coordinate coordinates and timestamps to support rapid spatial queries.
- Seeding scripts containing simulated coordinate grids for test scenarios.
