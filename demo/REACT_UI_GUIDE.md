# 🎨 React UI Guide - Agentic Mapping AI

## 📋 Overview

The React UI provides a modern, intuitive interface for the Agentic Mapping AI platform. It offers a comprehensive web-based experience for data transformation workflows.

## 🚀 Quick Start

### Option 1: Full Demo (Recommended)
```bash
# Start both API and UI together
python demo_launcher.py
# Select option 7: "🚀 Start Full Demo (API + UI)"
```

### Option 2: Start Components Separately
```bash
# Terminal 1: Start API Server
cd demo
python -m uvicorn agentic_mapping_ai.api.main:app --reload --port 8000

# Terminal 2: Start React UI
cd demo
python start_react_ui.py
```

## 🌐 Access Points

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 UI Features

### 🏠 Dashboard
- **Quick Actions**: Direct access to all major features
- **Workflow History**: Recent processing activities
- **System Status**: Real-time API connection status
- **Statistics**: Overview of completed workflows

### 📊 Excel Upload & Processing
- **Drag & Drop Interface**: Intuitive file upload
- **Progress Tracking**: Real-time upload and processing status
- **Sheet Validation**: Automatic detection of required sheets
- **Preview**: Sample data display and column mapping

### 🤖 Agent Workflow
- **Visual Progress**: Step-by-step workflow visualization
- **Configuration**: Customizable workflow parameters
- **Real-time Status**: Live updates during processing
- **Results Display**: Comprehensive output summary

### 🔍 Metadata Validation
- **Schema Validation**: Table structure verification
- **Data Quality**: Comprehensive quality checks
- **Error Reporting**: Detailed validation results
- **Recommendations**: Automated improvement suggestions

### 🧪 Test Generation
- **Automated Testing**: Comprehensive test suite creation
- **Coverage Analysis**: Test coverage reporting
- **Mock Data**: Sample data generation
- **Validation Rules**: Custom validation logic

## 🛠️ Technical Stack

### Frontend Technologies
- **React 18**: Modern React with hooks
- **Material-UI (MUI)**: Professional UI components
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **React Dropzone**: File upload functionality

### Development Tools
- **Create React App**: Development environment
- **React Scripts**: Build and development tools
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting (optional)

## 📂 Project Structure

```
react-ui/
├── public/
│   └── index.html              # Main HTML template
├── src/
│   ├── components/             # Reusable components
│   │   └── Navbar.js          # Navigation bar
│   ├── pages/                 # Page components
│   │   ├── Dashboard.js       # Main dashboard
│   │   ├── ExcelUpload.js     # File upload page
│   │   ├── AgentWorkflow.js   # Workflow management
│   │   ├── MetadataValidation.js
│   │   ├── TestGeneration.js
│   │   └── Settings.js
│   ├── utils/
│   │   └── api.js            # API communication
│   ├── App.js                # Main application
│   ├── index.js              # Entry point
│   └── index.css             # Global styles
├── package.json              # Dependencies
└── README.md                 # React-specific docs
```

## 🔧 Configuration

### Environment Variables
```bash
# In react-ui/.env (optional)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### API Integration
The UI automatically connects to the FastAPI backend through:
- **Proxy Configuration**: Requests to `/api` are proxied to port 8000
- **CORS Handling**: Backend configured for React development server
- **Error Handling**: Automatic retry and error display

## 🎯 Usage Scenarios

### 1. Data Mapping Workflow
```
Upload Excel → Configure Mapping → Run Agents → Review Results
```

### 2. Metadata Validation
```
Upload Schema → Validate Structure → Review Issues → Export Report
```

### 3. Test Generation
```
Select Code → Configure Tests → Generate Suite → Download Files
```

## 🐛 Troubleshooting

### Common Issues

#### 1. UI Won't Start
```bash
# Check Node.js installation
node --version
npm --version

# Clear cache and reinstall
cd react-ui
rm -rf node_modules package-lock.json
npm install
```

#### 2. API Connection Failed
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check network configuration
netstat -tlnp | grep 8000
```

#### 3. Build Errors
```bash
# Install with legacy peer deps
npm install --legacy-peer-deps

# Or use yarn instead
yarn install
```

#### 4. Port Conflicts
```bash
# Change React port
npm start -- --port 3001

# Or set environment variable
export PORT=3001
npm start
```

### Windows-Specific Issues

#### PowerShell Execution Policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Node.js Path Issues
```cmd
# Add Node.js to PATH
set PATH=%PATH%;C:\Program Files\nodejs\
```

## 🔄 Development Workflow

### 1. Making Changes
```bash
# The development server auto-reloads on changes
cd react-ui
npm start
# Edit files in src/ - changes appear immediately
```

### 2. Adding New Features
```bash
# Install additional packages
npm install package-name

# Add new components
mkdir src/components/NewComponent
```

### 3. Building for Production
```bash
cd react-ui
npm run build
# Creates optimized production build in build/
```

## 📊 Performance Tips

### Optimization
- **Code Splitting**: Pages are loaded on-demand
- **API Caching**: Responses cached for repeated requests
- **Image Optimization**: Compressed assets
- **Lazy Loading**: Components loaded when needed

### Development
- **Hot Reload**: Instant updates during development
- **Source Maps**: Debugging support
- **Error Boundaries**: Graceful error handling
- **TypeScript Ready**: Can be converted to TypeScript

## 🔐 Security Considerations

### Client-Side Security
- **Input Validation**: All user inputs validated
- **XSS Protection**: Content sanitized
- **CSRF Protection**: Token-based requests
- **Secure Headers**: Content Security Policy

### API Communication
- **Token Authentication**: Secure API access
- **HTTPS Ready**: Production-ready SSL support
- **Rate Limiting**: Request throttling
- **Error Sanitization**: No sensitive data in errors

## 📈 Future Enhancements

### Planned Features
- **Real-time Notifications**: WebSocket integration
- **Advanced Charts**: Data visualization with D3.js
- **Code Editor**: Syntax highlighting for generated code
- **Theme Switching**: Dark/light mode support
- **Internationalization**: Multi-language support

### Integration Opportunities
- **Database Connectivity**: Direct database schema import
- **Git Integration**: Version control for generated code
- **CI/CD Pipeline**: Automated deployment
- **Monitoring Dashboard**: System health metrics

## 🆘 Support

### Getting Help
1. **Check Console**: Browser developer tools for errors
2. **Network Tab**: Verify API requests
3. **Component State**: React Developer Tools
4. **Backend Logs**: Check API server output

### Resources
- **React Documentation**: https://reactjs.org/docs
- **Material-UI Guide**: https://mui.com/getting-started
- **API Documentation**: http://localhost:8000/docs
- **Demo Repository**: GitHub repository with examples

---

🎯 **Quick Test**: After starting the UI, visit http://localhost:3000 and try uploading an Excel file to verify everything is working correctly!
