# Frontend Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    React App                          │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │           App.jsx (Root Component)              │  │ │
│  │  │  - Orchestrates all components                  │  │ │
│  │  │  - Manages view switching                       │  │ │
│  │  └──────────────┬──────────────────────────────────┘  │ │
│  │                 │                                      │ │
│  │                 ▼                                      │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │   useDistanceCalculator (Custom Hook)           │  │ │
│  │  │  - State management                             │  │ │
│  │  │  - Business logic                               │  │ │
│  │  │  - API orchestration                            │  │ │
│  │  └───────┬────────────────────────┬─────────────────┘  │ │
│  │          │                        │                    │ │
│  │          ▼                        ▼                    │ │
│  │  ┌─────────────┐        ┌───────────────┐            │ │
│  │  │  ApiService │        │  Components   │            │ │
│  │  │  - HTTP     │        │  - Header     │            │ │
│  │  │  - Errors   │        │  - Form       │            │ │
│  │  │  - Transform│        │  - Map        │            │ │
│  │  └──────┬──────┘        │  - Error      │            │ │
│  │         │               │  - History    │            │ │
│  │         │               └───────────────┘            │ │
│  │         ▼                                             │ │
│  └─────────────────────────────────────────────────────┘  │
└─────────────┼───────────────────────────────────────────┘
              │ HTTP/JSON
              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API                              │
│               (Flask REST API)                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
App
├── Header
│   └── Button (View Toggle)
│
├── Main Form (Calculator View)
│   ├── CalculatorForm
│   │   ├── Source Input
│   │   ├── Destination Input
│   │   ├── Unit Radio Group
│   │   └── Calculate Button
│   ├── MapPlaceholder
│   └── ErrorToast
│
└── History View
    └── HistoryTable
        ├── Table Header
        └── Table Rows
```

## Data Flow Architecture

```
┌──────────────────────────────────────────────────┐
│              User Interaction                    │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│           Component Layer                        │
│  - CalculatorForm                                │
│  - Header                                        │
│  - HistoryTable                                  │
└──────────────────┬───────────────────────────────┘
                   │ Event Handlers
                   ▼
┌──────────────────────────────────────────────────┐
│         Custom Hook Layer                        │
│  useDistanceCalculator                           │
│  - State: source, destination, unit, etc.        │
│  - Actions: calculateDistance, toggleView        │
└──────────────────┬───────────────────────────────┘
                   │ API Calls
                   ▼
┌──────────────────────────────────────────────────┐
│           Service Layer                          │
│  ApiService                                      │
│  - calculateDistance()                           │
│  - fetchHistory()                                │
│  - healthCheck()                                 │
└──────────────────┬───────────────────────────────┘
                   │ HTTP
                   ▼
┌──────────────────────────────────────────────────┐
│              Backend API                         │
└──────────────────┬───────────────────────────────┘
                   │ Response
                   ▼
┌──────────────────────────────────────────────────┐
│         Service Layer                            │
│  - Parse response                                │
│  - Handle errors                                 │
│  - Transform data                                │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│         Custom Hook Layer                        │
│  - Update state                                  │
│  - Trigger re-render                             │
└──────────────────┬───────────────────────────────┘
                   │ Props
                   ▼
┌──────────────────────────────────────────────────┐
│          Component Layer                         │
│  - Re-render with new data                       │
│  - Display updated UI                            │
└──────────────────────────────────────────────────┘
```

