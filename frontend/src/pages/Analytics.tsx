import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';

const Analytics: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        실적 분석
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              KPI 분석
            </Typography>
            <Typography color="text.secondary">
              실적 분석 기능이 준비 중입니다.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;