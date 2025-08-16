import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens if needed
api.interceptors.request.use(
  (config) => {
    // Add auth header if token exists
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// API Health Check
export const checkApiHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('API Health Check Failed:', error);
    return false;
  }
};

// Excel File Upload
export const uploadExcelFile = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/v1/excel/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Excel Upload Failed:', error);
    throw error;
  }
};

// Process Excel File
export const processExcelFile = async (filename, options = {}) => {
  try {
    const response = await api.post('/api/v1/excel/process-full', {
      filename,
      ...options,
    });
    
    return response.data;
  } catch (error) {
    console.error('Excel Processing Failed:', error);
    throw error;
  }
};

// Agent Workflow API
export const startAgentWorkflow = async (workflowType, request) => {
  try {
    const response = await api.post(`/api/v1/agent/${workflowType}`, request);
    return response.data;
  } catch (error) {
    console.error('Agent Workflow Failed:', error);
    throw error;
  }
};

// Get Agent Status
export const getAgentStatus = async (taskId) => {
  try {
    const response = await api.get(`/api/v1/agent/status/${taskId}`);
    return response.data;
  } catch (error) {
    console.error('Agent Status Check Failed:', error);
    throw error;
  }
};

// Metadata Validation
export const validateMetadata = async (tableMetadata) => {
  try {
    const response = await api.post('/api/v1/metadata/validate', tableMetadata);
    return response.data;
  } catch (error) {
    console.error('Metadata Validation Failed:', error);
    throw error;
  }
};

// Generate PySpark Code
export const generatePySparkCode = async (mappingRequest) => {
  try {
    const response = await api.post('/api/v1/code-generation/pyspark', mappingRequest);
    return response.data;
  } catch (error) {
    console.error('Code Generation Failed:', error);
    throw error;
  }
};

// Generate Test Cases
export const generateTestCases = async (codeRequest) => {
  try {
    const response = await api.post('/api/v1/test-generation/generate', codeRequest);
    return response.data;
  } catch (error) {
    console.error('Test Generation Failed:', error);
    throw error;
  }
};

// Get Workflow History
export const getWorkflowHistory = async () => {
  try {
    const response = await api.get('/api/v1/workflow/history');
    return response.data;
  } catch (error) {
    console.error('Workflow History Failed:', error);
    throw error;
  }
};

// RAG Engine Search
export const searchKnowledge = async (query) => {
  try {
    const response = await api.post('/api/v1/rag/search', { query });
    return response.data;
  } catch (error) {
    console.error('Knowledge Search Failed:', error);
    throw error;
  }
};

// Chat with AI Agent
export const chatWithAgent = async (message, context = {}) => {
  try {
    const response = await api.post('/api/v1/chat/message', {
      message,
      context,
      timestamp: new Date().toISOString(),
    });
    return response.data;
  } catch (error) {
    console.error('Chat Failed:', error);
    throw error;
  }
};

// Get Chat History
export const getChatHistory = async () => {
  try {
    const response = await api.get('/api/v1/chat/history');
    return response.data;
  } catch (error) {
    console.error('Chat History Failed:', error);
    throw error;
  }
};

// Clear Chat Session
export const clearChatSession = async () => {
  try {
    const response = await api.delete('/api/v1/chat/session');
    return response.data;
  } catch (error) {
    console.error('Clear Chat Failed:', error);
    throw error;
  }
};

export default api;
