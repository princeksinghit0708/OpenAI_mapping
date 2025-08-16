import React, { useState, useEffect, useRef } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Box,
  Avatar,
  Chip,
  Button,
  Grid,
  Card,
  CardContent,
  Divider,
  IconButton,
  Tooltip,
  Alert,
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as UserIcon,
  Clear as ClearIcon,
  Lightbulb as SuggestionIcon,
  Upload as UploadIcon,
  Code as CodeIcon,
  CheckCircle as ValidateIcon,
  BugReport as TestIcon,
} from '@mui/icons-material';
import { chatWithAgent, uploadExcelFile, startAgentWorkflow } from '../utils/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [context, setContext] = useState({
    currentTask: null,
    uploadedFiles: [],
    workflowStatus: 'idle',
    lastAction: null,
  });
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Initial greeting
    addBotMessage(
      "👋 Hello! I'm your AI mapping assistant. I can help you with:\n\n" +
      "• Upload and analyze Excel mapping files\n" +
      "• Generate PySpark transformation code\n" +
      "• Create comprehensive test suites\n" +
      "• Validate metadata and data quality\n" +
      "• Run complete agent workflows\n\n" +
      "What would you like to do today? You can ask me in plain English!"
    );
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const addUserMessage = (text) => {
    const message = {
      id: Date.now(),
      type: 'user',
      content: text,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, message]);
  };

  const addBotMessage = (text, actionButtons = null, data = null) => {
    const message = {
      id: Date.now(),
      type: 'bot',
      content: text,
      timestamp: new Date(),
      actionButtons,
      data,
    };
    setMessages(prev => [...prev, message]);
  };

  const parseUserIntent = (text) => {
    const lowerText = text.toLowerCase();
    
    // Intent patterns
    const patterns = {
      upload: ['upload', 'load', 'import', 'file', 'excel', 'xlsx'],
      generate: ['generate', 'create', 'build', 'make', 'code', 'pyspark', 'transformation'],
      validate: ['validate', 'check', 'verify', 'quality', 'metadata', 'schema'],
      test: ['test', 'testing', 'test case', 'unit test', 'validation'],
      workflow: ['workflow', 'pipeline', 'process', 'run all', 'complete', 'end-to-end'],
      help: ['help', 'how', 'what', 'guide', 'tutorial', 'explain'],
      status: ['status', 'progress', 'what happened', 'result', 'how did it go'],
    };

    for (const [intent, keywords] of Object.entries(patterns)) {
      if (keywords.some(keyword => lowerText.includes(keyword))) {
        return intent;
      }
    }

    return 'general';
  };

  const generateResponse = async (userText, intent) => {
    setIsTyping(true);

    try {
      switch (intent) {
        case 'upload':
          return await handleUploadIntent(userText);
        case 'generate':
          return await handleGenerateIntent(userText);
        case 'validate':
          return await handleValidateIntent(userText);
        case 'test':
          return await handleTestIntent(userText);
        case 'workflow':
          return await handleWorkflowIntent(userText);
        case 'status':
          return await handleStatusIntent(userText);
        case 'help':
          return await handleHelpIntent(userText);
        default:
          return await handleGeneralIntent(userText);
      }
    } catch (error) {
      console.error('Error generating response:', error);
      return {
        text: "I apologize, but I encountered an error processing your request. Please try again or be more specific about what you'd like me to help you with.",
        actions: null,
      };
    } finally {
      setIsTyping(false);
    }
  };

  const handleUploadIntent = async (userText) => {
    return {
      text: "I'll help you upload your Excel mapping file! You have a few options:\n\n" +
            "1. **Drag & Drop**: Go to the Excel Upload page and drag your file\n" +
            "2. **File Browser**: Click the upload button to browse for your file\n" +
            "3. **Quick Setup**: I can guide you through the file requirements\n\n" +
            "Your file should be named `ebs_IM_account_DATAhub_mapping_v8.0.xlsx` and contain these sheets:\n" +
            "• `datahub standard mapping` (main mapping data)\n" +
            "• `goldref` (reference data)\n\n" +
            "What would you like to do?",
      actions: [
        { label: 'Go to Upload Page', action: 'navigate', target: '/upload' },
        { label: 'Check File Requirements', action: 'help', target: 'file_requirements' },
        { label: 'Setup Excel File', action: 'setup_excel' },
      ],
    };
  };

  const handleGenerateIntent = async (userText) => {
    if (context.uploadedFiles.length === 0) {
      return {
        text: "I'd love to help you generate code! However, I need an Excel mapping file first.\n\n" +
              "Please upload your mapping file, and then I can:\n" +
              "• Generate PySpark transformation code\n" +
              "• Create SQL transformations\n" +
              "• Build Python data processing scripts\n\n" +
              "Would you like to upload a file now?",
        actions: [
          { label: 'Upload File', action: 'navigate', target: '/upload' },
          { label: 'Use Sample Data', action: 'use_sample' },
        ],
      };
    }

    return {
      text: "Great! I can generate various types of code for you:\n\n" +
            "• **PySpark Transformations**: For big data processing\n" +
            "• **SQL Scripts**: For database transformations\n" +
            "• **Python Code**: For data manipulation\n\n" +
            "I'll analyze your mapping file and create optimized, production-ready code with:\n" +
            "✅ Error handling and validation\n" +
            "✅ Performance optimization\n" +
            "✅ Comprehensive documentation\n" +
            "✅ Best practices implementation\n\n" +
            "What type of code would you like me to generate?",
      actions: [
        { label: 'Generate PySpark', action: 'generate_code', target: 'pyspark' },
        { label: 'Generate SQL', action: 'generate_code', target: 'sql' },
        { label: 'Full Workflow', action: 'start_workflow', target: 'full_pipeline' },
      ],
    };
  };

  const handleValidateIntent = async (userText) => {
    return {
      text: "I'll help you validate your data! I can perform comprehensive checks:\n\n" +
            "🔍 **Metadata Validation**:\n" +
            "• Schema structure verification\n" +
            "• Data type consistency\n" +
            "• Column mapping accuracy\n" +
            "• Business rule compliance\n\n" +
            "🎯 **Data Quality Checks**:\n" +
            "• Null value analysis\n" +
            "• Data format validation\n" +
            "• Referential integrity\n" +
            "• Statistical profiling\n\n" +
            "What would you like me to validate?",
      actions: [
        { label: 'Validate Metadata', action: 'start_validation', target: 'metadata' },
        { label: 'Check Data Quality', action: 'start_validation', target: 'quality' },
        { label: 'Full Validation', action: 'start_workflow', target: 'validation_only' },
      ],
    };
  };

  const handleTestIntent = async (userText) => {
    return {
      text: "Excellent! I'll create comprehensive test suites for you:\n\n" +
            "🧪 **Test Types I Can Generate**:\n" +
            "• Unit tests for individual transformations\n" +
            "• Integration tests for end-to-end workflows\n" +
            "• Data quality tests with assertions\n" +
            "• Performance tests for large datasets\n" +
            "• Mock data generation for testing\n\n" +
            "📊 **What You'll Get**:\n" +
            "• Ready-to-run test files\n" +
            "• Sample test data\n" +
            "• Validation rules\n" +
            "• Coverage reports\n\n" +
            "What kind of tests do you need?",
      actions: [
        { label: 'Generate All Tests', action: 'generate_tests', target: 'comprehensive' },
        { label: 'Unit Tests Only', action: 'generate_tests', target: 'unit' },
        { label: 'Mock Data Only', action: 'generate_tests', target: 'mock_data' },
      ],
    };
  };

  const handleWorkflowIntent = async (userText) => {
    return {
      text: "Perfect! I'll run the complete end-to-end workflow for you:\n\n" +
            "🔄 **Full Pipeline Includes**:\n" +
            "1. 📊 **Metadata Extraction** - Analyze your Excel file\n" +
            "2. 🔧 **Code Generation** - Create PySpark transformations\n" +
            "3. 🧪 **Test Creation** - Generate comprehensive test suites\n" +
            "4. ✅ **Validation** - Quality checks and verification\n\n" +
            "⏱️ **Estimated Time**: 3-5 minutes\n" +
            "📁 **Output**: Generated code, tests, and documentation\n\n" +
            "Ready to start the complete workflow?",
      actions: [
        { label: 'Start Full Pipeline', action: 'start_workflow', target: 'full_mapping_pipeline' },
        { label: 'Code Generation Only', action: 'start_workflow', target: 'code_generation_only' },
        { label: 'Customize Workflow', action: 'navigate', target: '/agents' },
      ],
    };
  };

  const handleStatusIntent = async (userText) => {
    const statusText = context.workflowStatus === 'idle' 
      ? "No active workflows currently running."
      : context.workflowStatus === 'running'
      ? "Workflow is currently running. I'll keep you updated on progress!"
      : `Last workflow status: ${context.workflowStatus}`;

    return {
      text: `📊 **Current Status**:\n${statusText}\n\n` +
            `📁 **Uploaded Files**: ${context.uploadedFiles.length} file(s)\n` +
            `🔧 **Last Action**: ${context.lastAction || 'None'}\n\n` +
            "Is there anything specific you'd like me to check or help you with?",
      actions: [
        { label: 'Check Workflows', action: 'navigate', target: '/agents' },
        { label: 'View Dashboard', action: 'navigate', target: '/' },
      ],
    };
  };

  const handleHelpIntent = async (userText) => {
    return {
      text: "I'm here to help! Here's what I can assist you with:\n\n" +
            "🎯 **Main Capabilities**:\n" +
            "• **File Upload**: Help with Excel file requirements and upload\n" +
            "• **Code Generation**: Create PySpark, SQL, or Python transformations\n" +
            "• **Testing**: Generate comprehensive test suites\n" +
            "• **Validation**: Perform data quality and metadata checks\n" +
            "• **Workflows**: Run end-to-end processing pipelines\n\n" +
            "💡 **Tips**:\n" +
            "• Just tell me what you want in plain English\n" +
            "• I understand context from our conversation\n" +
            "• I can guide you step-by-step through any process\n\n" +
            "What specific help do you need?",
      actions: [
        { label: 'Getting Started Guide', action: 'help', target: 'getting_started' },
        { label: 'File Requirements', action: 'help', target: 'file_requirements' },
        { label: 'View Examples', action: 'help', target: 'examples' },
      ],
    };
  };

  const handleGeneralIntent = async (userText) => {
    // Use the existing chat API for general queries
    try {
      const response = await chatWithAgent(userText, context);
      return {
        text: response.message || "I understand you're asking about mapping and data transformation. Could you be more specific about what you'd like me to help you with?",
        actions: response.suggested_actions || [
          { label: 'Upload File', action: 'navigate', target: '/upload' },
          { label: 'Generate Code', action: 'help', target: 'generate' },
          { label: 'Run Workflow', action: 'navigate', target: '/agents' },
        ],
      };
    } catch (error) {
      return {
        text: "I'm here to help with data mapping and transformation tasks. You can ask me to:\n\n" +
              "• Upload and process Excel files\n" +
              "• Generate transformation code\n" +
              "• Create test suites\n" +
              "• Validate data quality\n" +
              "• Run complete workflows\n\n" +
              "What would you like to do?",
        actions: [
          { label: 'Upload File', action: 'navigate', target: '/upload' },
          { label: 'Generate Code', action: 'navigate', target: '/mapping' },
          { label: 'Run Workflow', action: 'navigate', target: '/agents' },
        ],
      };
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = inputText.trim();
    addUserMessage(userMessage);
    setInputText('');

    // Parse user intent
    const intent = parseUserIntent(userMessage);
    
    // Generate response
    const response = await generateResponse(userMessage, intent);
    
    // Add bot response
    addBotMessage(response.text, response.actions);
  };

  const handleActionClick = async (action) => {
    switch (action.action) {
      case 'navigate':
        window.location.href = action.target;
        break;
      case 'start_workflow':
        addBotMessage("🚀 Starting workflow... I'll keep you updated on the progress!");
        try {
          const result = await startAgentWorkflow(action.target, {
            excel_file: 'ebs_IM_account_DATAhub_mapping_v8.0.xlsx',
            workflow_type: action.target,
          });
          setContext(prev => ({ ...prev, workflowStatus: 'running', lastAction: 'workflow_started' }));
          addBotMessage(`✅ Workflow started successfully! Task ID: ${result.task_id}\n\nI'll monitor the progress and let you know when it's complete.`);
        } catch (error) {
          addBotMessage(`❌ Sorry, I couldn't start the workflow. Error: ${error.message}\n\nWould you like me to help you troubleshoot this?`);
        }
        break;
      case 'generate_code':
        addBotMessage(`🔧 Generating ${action.target} code... This may take a moment.`);
        // Implement code generation logic
        break;
      case 'setup_excel':
        addBotMessage("📊 Let me guide you through setting up your Excel file correctly...", [
          { label: 'Show Requirements', action: 'help', target: 'file_requirements' },
          { label: 'Download Template', action: 'download_template' },
        ]);
        break;
      default:
        addBotMessage("I'm processing your request...");
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setContext({
      currentTask: null,
      uploadedFiles: [],
      workflowStatus: 'idle',
      lastAction: null,
    });
  };

  const quickSuggestions = [
    "Upload my Excel mapping file",
    "Generate PySpark transformation code",
    "Run the complete workflow",
    "Validate my data quality",
    "Create test cases for my transformations",
    "Help me get started",
  ];

  return (
    <Container maxWidth="lg" className="fade-in">
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        💬 AI Chat Assistant
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Chat with your AI assistant in plain English. Ask questions, request help, or describe what you want to accomplish!
      </Typography>

      <Grid container spacing={3}>
        {/* Chat Area */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
            {/* Chat Header */}
            <Box sx={{ p: 2, borderBottom: '1px solid #e0e0e0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <BotIcon color="primary" />
                <Typography variant="h6">AI Mapping Assistant</Typography>
                <Chip label="Online" color="success" size="small" />
              </Box>
              <Tooltip title="Clear conversation">
                <IconButton onClick={clearChat}>
                  <ClearIcon />
                </IconButton>
              </Tooltip>
            </Box>

            {/* Messages */}
            <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
              {messages.map((message) => (
                <Box
                  key={message.id}
                  sx={{
                    display: 'flex',
                    justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                    mb: 2,
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, maxWidth: '80%' }}>
                    {message.type === 'bot' && (
                      <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                        <BotIcon fontSize="small" />
                      </Avatar>
                    )}
                    
                    <Box>
                      <Paper
                        sx={{
                          p: 2,
                          backgroundColor: message.type === 'user' ? 'primary.main' : 'grey.100',
                          color: message.type === 'user' ? 'white' : 'text.primary',
                        }}
                      >
                        <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                          {message.content}
                        </Typography>
                      </Paper>
                      
                      {/* Action Buttons */}
                      {message.actionButtons && (
                        <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          {message.actionButtons.map((action, index) => (
                            <Button
                              key={index}
                              variant="outlined"
                              size="small"
                              onClick={() => handleActionClick(action)}
                              startIcon={
                                action.action === 'navigate' ? <UploadIcon /> :
                                action.action === 'start_workflow' ? <CodeIcon /> :
                                action.action === 'generate_code' ? <CodeIcon /> :
                                <SuggestionIcon />
                              }
                            >
                              {action.label}
                            </Button>
                          ))}
                        </Box>
                      )}
                      
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                        {message.timestamp.toLocaleTimeString()}
                      </Typography>
                    </Box>
                    
                    {message.type === 'user' && (
                      <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
                        <UserIcon fontSize="small" />
                      </Avatar>
                    )}
                  </Box>
                </Box>
              ))}
              
              {isTyping && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                    <BotIcon fontSize="small" />
                  </Avatar>
                  <Paper sx={{ p: 2, backgroundColor: 'grey.100' }}>
                    <Typography variant="body2" color="text.secondary">
                      AI is thinking...
                    </Typography>
                  </Paper>
                </Box>
              )}
              
              <div ref={messagesEndRef} />
            </Box>

            {/* Input Area */}
            <Box sx={{ p: 2, borderTop: '1px solid #e0e0e0' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  multiline
                  maxRows={3}
                  placeholder="Ask me anything about data mapping and transformation..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={isTyping}
                />
                <Button
                  variant="contained"
                  onClick={handleSendMessage}
                  disabled={!inputText.trim() || isTyping}
                  sx={{ minWidth: 'auto', px: 2 }}
                >
                  <SendIcon />
                </Button>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Quick Suggestions */}
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                💡 Quick Suggestions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                {quickSuggestions.map((suggestion, index) => (
                  <Button
                    key={index}
                    variant="outlined"
                    size="small"
                    onClick={() => {
                      setInputText(suggestion);
                      handleSendMessage();
                    }}
                    sx={{ justifyContent: 'flex-start', textTransform: 'none' }}
                  >
                    {suggestion}
                  </Button>
                ))}
              </Box>
            </CardContent>
          </Card>

          {/* Context Info */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📊 Current Context
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Workflow Status:
                  </Typography>
                  <Chip
                    label={context.workflowStatus}
                    color={
                      context.workflowStatus === 'running' ? 'warning' :
                      context.workflowStatus === 'completed' ? 'success' : 'default'
                    }
                    size="small"
                  />
                </Box>
                
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Uploaded Files:
                  </Typography>
                  <Typography variant="body1">
                    {context.uploadedFiles.length || 0} file(s)
                  </Typography>
                </Box>
                
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Last Action:
                  </Typography>
                  <Typography variant="body1">
                    {context.lastAction || 'None'}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Help Alert */}
      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>💡 Pro Tips:</strong> You can ask me anything in natural language! 
          Try phrases like "I need help uploading my file" or "Generate PySpark code for my mappings" 
          or "Run the complete workflow for me".
        </Typography>
      </Alert>
    </Container>
  );
};

export default ChatInterface;
