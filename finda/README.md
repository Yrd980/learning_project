# React TypeScript Vite Template

A modern, production-ready React TypeScript template with Vite, featuring comprehensive tooling and best practices.

## 🚀 Features

- **Core Framework**: React 19 with TypeScript
- **Build Tool**: Vite for fast development and optimized builds
- **Routing**: React Router DOM v7 for client-side routing
- **State Management**: Zustand for lightweight state management
- **Data Fetching**: TanStack Query (React Query) for server state management
- **HTTP Client**: Axios with interceptors and error handling
- **Styling**: Tailwind CSS v4 with custom design system
- **UI Components**: Headless UI for accessible components
- **Icons**: Lucide React for beautiful icons
- **Animations**: Framer Motion for smooth animations
- **Code Quality**: ESLint + Prettier for consistent code formatting
- **Testing**: Jest + React Testing Library for comprehensive testing
- **Type Safety**: Full TypeScript support with strict configuration
- **Backend Integration**: Built-in proxy for local backend development

## 📦 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.1.0 | UI Framework |
| TypeScript | 5.8.3 | Type Safety |
| Vite | 7.0.4 | Build Tool & Dev Server |
| React Router | 7.7.0 | Client-side Routing |
| Zustand | 5.0.6 | State Management |
| TanStack Query | 5.59.16 | Server State Management |
| Axios | 1.10.0 | HTTP Client |
| Tailwind CSS | 4.1.11 | Utility-first CSS |
| Headless UI | 2.2.4 | Accessible Components |
| Framer Motion | 12.23.6 | Animations |
| Jest | 30.0.4 | Testing Framework |
| ESLint | 9.31.0 | Code Linting |
| Prettier | 3.6.2 | Code Formatting |

## 🛠️ Getting Started

### Prerequisites

- Node.js 18+ (recommended: Node.js 22)
- npm, yarn, or pnpm
- Backend server running on `localhost:8080` (optional)

### Installation

1. **Clone the template**
   ```bash
   git clone <repository-url>
   cd react-typescript-vite-template
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local` with your configuration:
   ```env
   # API Configuration
   VITE_API_BASE_URL=/api
   VITE_API_TIMEOUT=10000
   
   # App Configuration
   VITE_APP_NAME=My App
   VITE_APP_VERSION=1.0.0
   
   # Backend Configuration
   VITE_BACKEND_URL=http://localhost:8080
   
   # Feature Flags
   VITE_ENABLE_ANALYTICS=false
   VITE_ENABLE_DEBUG=true
   VITE_ENABLE_MOCK_API=false
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🔧 Backend Integration

This template is configured to work with a backend server running on `localhost:8080`. The Vite development server includes a proxy that forwards all `/api/*` requests to your backend, avoiding CORS issues during development.

### Proxy Configuration

```javascript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
      secure: false,
      rewrite: (path) => path.replace(/^\/api/, '/api'),
    },
  },
}
```

### API Calls

All API calls in the template use relative paths that are automatically proxied:

```typescript
// This call to /api/users will be proxied to http://localhost:8080/api/users
const users = await api.get('/users');
```

### Backend Requirements

Your backend should:
- Run on `localhost:8080`
- Have API endpoints under `/api/*`
- Return JSON responses
- Handle CORS properly (or rely on the proxy)

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Shared components (Button, Input, etc.)
│   ├── features/       # Feature-specific components
│   └── layout/         # Layout components
├── hooks/              # Custom React hooks
├── pages/              # Page components
├── queries/            # TanStack Query hooks
├── routes/             # Route definitions
├── services/           # API services and utilities
├── store/              # Zustand stores
├── styles/             # Global styles and CSS modules
├── types/              # TypeScript type definitions
└── utils/              # Utility functions
```

## 🎯 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix ESLint errors |
| `npm run format` | Format code with Prettier |
| `npm run format:check` | Check code formatting |
| `npm run type-check` | Run TypeScript type checking |
| `npm run test` | Run tests |
| `npm run test:watch` | Run tests in watch mode |
| `npm run test:coverage` | Run tests with coverage |

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the root directory:

```env
# API Configuration
VITE_API_BASE_URL=/api
VITE_API_TIMEOUT=10000

# App Configuration
VITE_APP_NAME=My App
VITE_APP_VERSION=1.0.0

# Backend Configuration
VITE_BACKEND_URL=http://localhost:8080

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
VITE_ENABLE_MOCK_API=false
```

## 📊 State Management

### Zustand Store Example

```typescript
// src/store/userStore.ts
import { create } from 'zustand';

interface UserState {
  user: User | null;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isLoading: false,
  setUser: (user) => set({ user }),
  setLoading: (isLoading) => set({ isLoading }),
}));
```

### TanStack Query Example

```typescript
// src/queries/useUsersQuery.ts
import { useQuery } from '@tanstack/react-query';
import { userApi } from '../services/api';

export const useUsers = (filters = {}) => {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => userApi.getUsers(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};
```

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts

### Deploy to Netlify

1. Build the project: `npm run build`
2. Deploy the `dist/` folder to Netlify

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Vite](https://vitejs.dev/) for the amazing build tool
- [TanStack](https://tanstack.com/) for React Query
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Zustand](https://github.com/pmndrs/zustand) for lightweight state management

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.
