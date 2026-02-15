# Distance Calculator Frontend - Modular Architecture

A well-structured, modular React frontend following industry best practices.

## Architecture Overview

The frontend follows a component-based modular architecture with clear separation of concerns:

```
frontend_modular/
├── public/
│   └── index.html
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Header/
│   │   │   ├── Header.jsx
│   │   │   ├── Header.css
│   │   │   └── index.js
│   │   ├── CalculatorForm/
│   │   │   ├── CalculatorForm.jsx
│   │   │   ├── CalculatorForm.css
│   │   │   └── index.js
│   │   ├── MapPlaceholder/
│   │   │   ├── MapPlaceholder.jsx
│   │   │   ├── MapPlaceholder.css
│   │   │   └── index.js
│   │   ├── ErrorToast/
│   │   │   ├── ErrorToast.jsx
│   │   │   ├── ErrorToast.css
│   │   │   └── index.js
│   │   └── HistoryTable/
│   │       ├── HistoryTable.jsx
│   │       ├── HistoryTable.css
│   │       └── index.js
│   ├── hooks/               # Custom React hooks
│   │   └── useDistanceCalculator.js
│   ├── services/            # API and external services
│   │   └── ApiService.js
│   ├── App.jsx              # Main application component
│   ├── App.css              # Global styles
│   └── index.js             # Application entry point
└── package.json
```

## Module Descriptions

### Components (`/src/components`)

#### **Header**
- **Purpose**: Application header with title and view toggle
- **Props**: `showHistory`, `onToggleView`
- **Responsibilities**: Display title, subtitle, navigation button

#### **CalculatorForm**
- **Purpose**: Main distance calculation form
- **Props**: `source`, `destination`, `unit`, `loading`, `distance`, handlers
- **Responsibilities**: User input, unit selection, form submission, distance display

#### **MapPlaceholder**
- **Purpose**: Visual map representation with marker
- **Props**: `show`
- **Responsibilities**: Display map when calculation completes

#### **ErrorToast**
- **Purpose**: Error notification display
- **Props**: `error`, `onClose`
- **Responsibilities**: Show/hide error messages, user dismissal

#### **HistoryTable**
- **Purpose**: Display historical queries in table format
- **Props**: `queries`
- **Responsibilities**: Render query history, handle empty state

### Custom Hooks (`/src/hooks`)

#### **useDistanceCalculator**
- **Purpose**: Encapsulate all calculator business logic
- **Returns**: State and action methods
- **Responsibilities**: 
  - Manage form state
  - Handle API calls
  - Control view switching
  - Error handling

### Services (`/src/services`)

#### **ApiService**
- **Purpose**: Centralize all API communications
- **Methods**: `calculateDistance()`, `fetchHistory()`, `healthCheck()`
- **Responsibilities**: HTTP requests, error handling, data transformation

### Main App (`/src`)

#### **App.jsx**
- **Purpose**: Application orchestrator
- **Responsibilities**: Coordinate components, manage routing between views

#### **App.css**
- **Purpose**: Global application styles
- **Scope**: Reset, layout, container styles

## Getting Started

### Installation
```bash
cd frontend_modular
npm install
```

### Running
```bash
npm start
```

The app will open at `http://localhost:3000`

### Building for Production
```bash
npm run build
```

## Design Patterns Used

### 1. **Component Composition**
Small, focused components that do one thing well.

### 2. **Custom Hooks**
Business logic extracted into reusable hooks.

### 3. **Service Layer**
API calls separated from UI components.

### 4. **Presentational vs Container Components**
- Presentational: Header, CalculatorForm, MapPlaceholder, etc.
- Container: App.jsx (coordinates everything)

### 5. **Single Responsibility Principle**
Each module has one clear purpose.

## Component API

### Header Component
```jsx
<Header 
  showHistory={boolean}
  onToggleView={function}
/>
```

### CalculatorForm Component
```jsx
<CalculatorForm
  source={string}
  destination={string}
  unit={string}
  loading={boolean}
  distance={object}
  onSourceChange={function}
  onDestinationChange={function}
  onUnitChange={function}
  onSubmit={function}
/>
```

### MapPlaceholder Component
```jsx
<MapPlaceholder 
  show={boolean}
/>
```

### ErrorToast Component
```jsx
<ErrorToast 
  error={string}
  onClose={function}
/>
```

### HistoryTable Component
```jsx
<HistoryTable 
  queries={array}
/>
```

## Extending the Application

### Adding a New Component

1. Create component folder:
```bash
mkdir src/components/MyComponent
```

2. Create files:
```jsx
// MyComponent.jsx
import React from 'react';
import './MyComponent.css';

const MyComponent = ({ prop1, prop2 }) => {
  return (
    <div className="my-component">
      {/* Component content */}
    </div>
  );
};

export default MyComponent;
```

3. Create styles:
```css
/* MyComponent.css */
.my-component {
  /* Styles */
}
```

4. Create index:
```js
// index.js
export { default } from './MyComponent';
```

5. Use in App:
```jsx
import MyComponent from './components/MyComponent';

<MyComponent prop1="value" prop2="value" />
```

### Adding a New Custom Hook

1. Create hook file in `/src/hooks/`:
```jsx
// useMyHook.js
import { useState, useEffect } from 'react';

const useMyHook = () => {
  const [state, setState] = useState(null);

  useEffect(() => {
    // Side effects
  }, []);

  return {
    state,
    setState,
  };
};

export default useMyHook;
```

2. Import and use:
```jsx
import useMyHook from './hooks/useMyHook';

const { state, setState } = useMyHook();
```



## Benefits of Modular Architecture

**Easier Testing**: Test components in isolation
**Better Collaboration**: Multiple developers can work simultaneously
**Code Reusability**: Components can be used in other projects
**Easier Debugging**: Issues isolated to specific modules
**Better IDE Support**: Better autocomplete and navigation
**Scalability**: Easy to add new features
**Maintainability**: Changes are localized

