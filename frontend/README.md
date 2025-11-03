# Hierarchical Todo App - Frontend

Beautiful, modern React + TypeScript frontend for the hierarchical todo list application.

## 🚀 Tech Stack

- **React 18** - Latest React with hooks
- **TypeScript** - Type safety
- **Vite** - Ultra-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Hot Toast** - Beautiful notifications
- **React Beautiful DnD** - Drag and drop

## 📦 Installation

### 1. Navigate to frontend directory
```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application\frontend"
```

### 2. Install dependencies
```powershell
npm install
```

## 🏃 Running the App

### Development Mode (with hot reload)
```powershell
npm run dev
```

The app will run on **http://localhost:3000**

### Build for Production
```powershell
npm run build
```

### Preview Production Build
```powershell
npm run preview
```

## 🎨 Features

### Authentication
- ✅ Beautiful login/register forms
- ✅ Session-based authentication
- ✅ Persistent sessions
- ✅ Protected routes

### Todo Lists
- ✅ Create, edit, delete lists
- ✅ View all your lists
- ✅ Search and filter

### Hierarchical Tasks
- ✅ Unlimited nesting (recursive rendering)
- ✅ Expand/collapse nodes
- ✅ Mark as complete
- ✅ Drag and drop reordering
- ✅ Beautiful animations
- ✅ Responsive design

### UI/UX
- ✅ Modern glassmorphism design
- ✅ Smooth transitions
- ✅ Loading states
- ✅ Error handling
- ✅ Toast notifications
- ✅ Responsive mobile design
- ✅ Dark mode ready

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── auth/          # Login, Register
│   │   ├── tasks/         # TaskList, TaskItem, TaskForm
│   │   ├── layout/        # Header, Sidebar, Layout
│   │   └── common/        # Button, Input, Modal, etc.
│   ├── contexts/          # React Context (Auth, Tasks)
│   ├── services/          # API services
│   ├── types/             # TypeScript interfaces
│   ├── utils/             # Helper functions
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── public/                # Static assets
├── index.html             # HTML template
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies
```

## 🔗 API Integration

The frontend connects to the Flask backend at:
```
http://127.0.0.1:5000/api
```

Make sure the backend server is running before starting the frontend!

## 🎯 Usage

1. **Start the backend server:**
   ```powershell
   cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
   python3 app.py
   ```

2. **Start the frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Open browser:**
   Navigate to http://localhost:3000

4. **Login with demo account:**
   - Username: `john_doe`
   - Password: `password123`

## 🎨 Customization

### Theme Colors
Edit `tailwind.config.js` to customize colors:
```javascript
theme: {
  extend: {
    colors: {
      primary: { ... },
      accent: { ... },
    },
  },
}
```

### API URL
Edit `.env` to change backend URL:
```
VITE_API_BASE_URL=http://your-api-url.com/api
```

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🐛 Troubleshooting

### Port 3000 already in use
Change the port in `vite.config.ts`:
```typescript
server: {
  port: 3001, // Change port
}
```

### Cannot connect to backend
- Ensure backend is running on http://127.0.0.1:5000
- Check `.env` file for correct API URL
- Check browser console for CORS errors

## 🚀 Deployment

### Build
```powershell
npm run build
```

The build output will be in the `dist/` folder, ready to deploy to any static hosting service (Netlify, Vercel, GitHub Pages, etc.).

### Environment Variables
For production, set:
```
VITE_API_BASE_URL=https://your-production-api.com/api
```

## 📄 License

Part of CS162 Web Application Assignment
