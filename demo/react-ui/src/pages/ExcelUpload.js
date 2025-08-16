import React, { useState, useCallback } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Alert,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { uploadExcelFile, processExcelFile } from '../utils/api';

const ExcelUpload = () => {
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, uploaded, processing, completed, error
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [processingResult, setProcessingResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploadStatus('uploading');
    setError(null);
    setUploadedFile(file);

    try {
      const result = await uploadExcelFile(file);
      setUploadResult(result);
      setUploadStatus('uploaded');
      
      // Auto-process the file
      await processFile(result.filename);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
      setUploadStatus('error');
    }
  }, []);

  const processFile = async (filename) => {
    setUploadStatus('processing');
    setError(null);

    try {
      const result = await processExcelFile(filename, {
        mapping_sheet: 'datahub standard mapping',
        goldref_sheet: 'goldref',
        auto_detect_columns: true,
      });
      
      setProcessingResult(result);
      setUploadStatus('completed');
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Processing failed');
      setUploadStatus('error');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
    },
    maxFiles: 1,
    disabled: uploadStatus === 'uploading' || uploadStatus === 'processing',
  });

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'uploaded':
      case 'completed':
        return <SuccessIcon color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const getStatusText = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'Uploading file...';
      case 'uploaded':
        return 'File uploaded successfully';
      case 'processing':
        return 'Processing Excel file...';
      case 'completed':
        return 'Processing completed successfully';
      case 'error':
        return 'Error occurred';
      default:
        return 'Ready to upload';
    }
  };

  return (
    <Container maxWidth="lg" className="fade-in">
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        📊 Excel File Upload & Processing
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom sx={{ mb: 4 }}>
        Upload your Excel mapping file to get started with data transformation
      </Typography>

      {/* Upload Area */}
      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          textAlign: 'center',
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
          cursor: uploadStatus === 'uploading' || uploadStatus === 'processing' ? 'not-allowed' : 'pointer',
          transition: 'all 0.2s ease',
          mb: 3,
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'action.hover',
          },
        }}
      >
        <input {...getInputProps()} />
        
        <UploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
        
        <Typography variant="h6" gutterBottom>
          {isDragActive ? 'Drop your Excel file here' : 'Drag & drop Excel file here'}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Supports .xlsx and .xls files • Maximum file size: 50MB
        </Typography>
        
        <Button
          variant="outlined"
          sx={{ mt: 2 }}
          disabled={uploadStatus === 'uploading' || uploadStatus === 'processing'}
        >
          Choose File
        </Button>
      </Paper>

      {/* Upload Progress */}
      {(uploadStatus === 'uploading' || uploadStatus === 'processing') && (
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            {getStatusIcon()}
            <Typography variant="body2" sx={{ ml: 1 }}>
              {getStatusText()}
            </Typography>
          </Box>
          <LinearProgress />
        </Box>
      )}

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <Typography variant="body2">
            {error}
          </Typography>
        </Alert>
      )}

      {/* Upload Result */}
      {uploadResult && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              📁 File Upload Details
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Filename: {uploadedFile?.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Size: {(uploadedFile?.size / 1024 / 1024).toFixed(2)} MB
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Upload ID: {uploadResult.upload_id}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Status: <Chip label="Uploaded" color="success" size="small" />
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Processing Result */}
      {processingResult && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              ⚡ Processing Results
            </Typography>
            
            {/* Summary Stats */}
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    {processingResult.total_mappings || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Mappings
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">
                    {processingResult.sheets_found || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Sheets Found
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="warning.main">
                    {processingResult.goldref_mappings || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Goldref Mappings
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="info.main">
                    {processingResult.complex_mappings || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Complex Mappings
                  </Typography>
                </Box>
              </Grid>
            </Grid>

            {/* Sheet Information */}
            {processingResult.sheets_info && (
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Sheet Name</TableCell>
                      <TableCell align="right">Rows</TableCell>
                      <TableCell align="right">Columns</TableCell>
                      <TableCell>Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(processingResult.sheets_info).map(([sheetName, info]) => (
                      <TableRow key={sheetName}>
                        <TableCell component="th" scope="row">
                          {sheetName}
                        </TableCell>
                        <TableCell align="right">{info.rows}</TableCell>
                        <TableCell align="right">{info.columns}</TableCell>
                        <TableCell>
                          <Chip
                            label={info.status || 'Processed'}
                            color="success"
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}

            {/* Next Steps */}
            <Alert severity="success" sx={{ mt: 3 }}>
              <Typography variant="body2">
                <strong>✅ Ready for next step!</strong> Your Excel file has been processed successfully. 
                You can now proceed to generate mappings or run the agent workflow.
              </Typography>
            </Alert>
          </CardContent>
        </Card>
      )}

      {/* Help Section */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          📋 Excel File Requirements
        </Typography>
        
        <Alert severity="info">
          <Typography variant="body2" component="div">
            <strong>Required Sheets:</strong>
            <ul>
              <li><strong>datahub standard mapping</strong> - Main mapping configuration</li>
              <li><strong>goldref</strong> - Reference data for derived mappings</li>
            </ul>
            
            <strong>Expected Columns:</strong>
            <ul>
              <li>Standard Physical Table Name, Standard Physical Column Name</li>
              <li>Source Table Name, Source Column Name</li>
              <li>Direct/Derived/Default/No Mapping, Transformation/Derivation</li>
            </ul>
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};

export default ExcelUpload;
