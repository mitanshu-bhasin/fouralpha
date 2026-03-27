# NEP 2030 Architecture & Deliverables

## 1. URL Slug Structure
SEO-friendly, nested URL paths ensuring logical grouping under the main `nep-2030` hub.

**Base Path:** `/education-policy/national/nep-2030`

**Verticals:**
- `/excellence/process`
- `/excellence/behavioral`
- `/excellence/academic`
- `/excellence/knowledge-management`
- `/excellence/healthcare`
- `/excellence/global-diplomacy`

**Complete Hierarchy Example (Healthcare):**
- **Vertical Level:** `/education-policy/national/nep-2030/excellence/healthcare`
- **Main Committee:** `/excellence/healthcare/committees/main`
- **Curriculum Sub-Committee:** `/excellence/healthcare/committees/curriculum`
- **Cells Sub-Committee (Schools):** `/excellence/healthcare/cells/schools`
- **Cells Sub-Committee (Colleges):** `/excellence/healthcare/cells/colleges`
- **Cells Sub-Committee (Universities):** `/excellence/healthcare/cells/universities`
- **Cells Sub-Committee (Research Institutions):** `/excellence/healthcare/cells/research-institutions`
- **Ambassadors Sub-Committee:** `/excellence/healthcare/ambassadors`

---

## 2. Breadcrumb Architecture
Logical trail for a user deep-diving into the 'Research Institutions' cell of the 'Healthcare' vertical.

```text
Home > Education Policy > National > NEP 2030 > Excellence Verticals > Healthcare > Cells > Research Institutions
```

**JSON-LD Schema for SEO (BreadcrumbList):**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.fouralpha.org/" },
    { "@type": "ListItem", "position": 2, "name": "Education Policy", "item": "https://www.fouralpha.org/education-policy" },
    { "@type": "ListItem", "position": 3, "name": "National", "item": "https://www.fouralpha.org/education-policy/national" },
    { "@type": "ListItem", "position": 4, "name": "NEP 2030", "item": "https://www.fouralpha.org/education-policy/national/nep-2030.html" },
    { "@type": "ListItem", "position": 5, "name": "Healthcare Vertical", "item": "https://www.fouralpha.org/education-policy/national/nep-2030/excellence/healthcare" },
    { "@type": "ListItem", "position": 6, "name": "Cells Sub-Committee", "item": "https://www.fouralpha.org/education-policy/national/nep-2030/excellence/healthcare/cells" },
    { "@type": "ListItem", "position": 7, "name": "Research Institutions", "item": "https://www.fouralpha.org/education-policy/national/nep-2030/excellence/healthcare/cells/research-institutions" }
  ]
}
```

---

## 3. Mega-Menu Wireframe (Text-based)
A clean, 3-column UI layout to be integrated into the navigation bar or main page structural layout.

**[NEP 2030 EXCELLENCE VERTICALS]** (Hover/Click to open)

| Column 1: Core Drivers                 | Column 2: Applied Excellence           | Column 3: Structural Breakdown (Selected Vertical) |
|----------------------------------------|----------------------------------------|----------------------------------------------------|
| **Process Excellence**                 | **Knowledge Management**               | **➔ Current Vertical:** [Hovered Vertical]         |
| Lean systems & optimized workflows     | Decentralized cognitive repositories   |                                                    |
|                                        |                                        | **Committees & Sub-Committees:**                   |
| **Behavioral Excellence**              | **Healthcare Excellence**              | ▫ Main Committee (12 Members)                      |
| Alpha metrics & behavioral alignment   | Biopsychosocial health optimization    | ▫ Curriculum Development (12 Members)              |
|                                        |                                        |                                                    |
| **Academic Excellence**                | **Global Diplomacy**                   | **Action Cells (Target Audiences):**               |
| Next-Gen pedagogical frameworks        | Cross-border alignment protocols       | ▫ Schools  \|  ▫ Colleges                          |
|                                        |                                        | ▫ Universities \|  ▫ Research Institutions         |
|                                        |                                        |                                                    |
|                                        |                                        | **Ambassadors Network:**                           |
|                                        |                                        | ▫ Global Cadre: Target 1M/Country                  |

*Behavior: Hovering over any item in Columns 1 or 2 updates Column 3 dynamically with detailed statistics or links.*

---

## 4. Database Taxonomy Schema (JSON & SQL)

### JSON Structure (NoSQL / Document DB)
```json
{
  "verticals": [
    {
      "id": "v_healthcare",
      "name": "Healthcare Excellence",
      "slug": "healthcare",
      "description": "Biopsychosocial health optimization",
      "structure": {
        "main_committee": {
          "id": "mc_healthcare",
          "member_capacity": 12,
          "name": "Healthcare Main Committee"
        },
        "curriculum_committee": {
          "id": "cc_healthcare",
          "member_capacity": 12,
          "name": "Healthcare Curriculum Sub-Committee"
        },
        "cells": [
          { "id": "cell_hc_schools", "target": "Schools", "slug": "schools" },
          { "id": "cell_hc_colleges", "target": "Colleges", "slug": "colleges" },
          { "id": "cell_hc_universities", "target": "Universities", "slug": "universities" },
          { "id": "cell_hc_research", "target": "Research Institutions", "slug": "research-institutions" }
        ],
        "ambassadors_committee": {
          "id": "ac_healthcare",
          "target_per_country": 1000000,
          "name": "Healthcare Ambassadors Network"
        }
      }
    }
  ]
}
```

### Relational Schema (SQL)
```sql
-- Core Verticals
CREATE TABLE nep_verticals (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL, -- e.g., 'Healthcare Excellence'
    slug VARCHAR(255) UNIQUE NOT NULL
);

-- Committees (Main & Curriculum)
CREATE TABLE nep_committees (
    id UUID PRIMARY KEY,
    vertical_id UUID REFERENCES nep_verticals(id),
    type VARCHAR(50) NOT NULL, -- 'MAIN', 'CURRICULUM'
    member_capacity INT DEFAULT 12,
    name VARCHAR(255) NOT NULL
);

-- Target Cells
CREATE TABLE nep_cells (
    id UUID PRIMARY KEY,
    vertical_id UUID REFERENCES nep_verticals(id),
    target_audience VARCHAR(100) NOT NULL, -- 'Schools', 'Colleges', 'Universities', 'Research Institutions'
    slug VARCHAR(100) NOT NULL
);

-- Ambassadors Target
CREATE TABLE nep_ambassadors (
    id UUID PRIMARY KEY,
    vertical_id UUID REFERENCES nep_verticals(id),
    target_per_country INT DEFAULT 1000000,
    name VARCHAR(255)
);
```
