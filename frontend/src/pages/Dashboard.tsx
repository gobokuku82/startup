import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Description,
  CheckCircle,
  Warning,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import useAuthStore from '@store/authStore';

// Mock data for charts
const salesData = [
  { month: '1월', revenue: 120000000, target: 100000000 },
  { month: '2월', revenue: 135000000, target: 110000000 },
  { month: '3월', revenue: 145000000, target: 120000000 },
  { month: '4월', revenue: 160000000, target: 130000000 },
  { month: '5월', revenue: 155000000, target: 140000000 },
  { month: '6월', revenue: 170000000, target: 150000000 },
];

const clientData = [
  { name: 'Seoul Medical', value: 35 },
  { name: 'Busan Clinic', value: 25 },
  { name: 'Daegu Pharmacy', value: 20 },
  { name: 'Others', value: 20 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

interface StatCard {
  title: string;
  value: string | number;
  change?: number;
  icon: React.ReactNode;
  color: string;
}

const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<StatCard[]>([]);

  useEffect(() => {
    // Mock stats data
    setStats([
      {
        title: '이번 달 매출',
        value: '₩170M',
        change: 9.5,
        icon: <TrendingUp />,
        color: '#4caf50',
      },
      {
        title: '활성 거래처',
        value: 45,
        change: 3,
        icon: <People />,
        color: '#2196f3',
      },
      {
        title: '생성 문서',
        value: 28,
        icon: <Description />,
        color: '#ff9800',
      },
      {
        title: '규정 준수율',
        value: '96%',
        icon: <CheckCircle />,
        color: '#4caf50',
      },
    ]);
  }, []);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        대시보드
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom>
        안녕하세요, {user?.email}님! 오늘의 비즈니스 현황입니다.
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mt: 1, mb: 3 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 2,
                      backgroundColor: `${stat.color}20`,
                      color: stat.color,
                      mr: 2,
                    }}
                  >
                    {stat.icon}
                  </Box>
                  <Typography color="text.secondary" variant="body2">
                    {stat.title}
                  </Typography>
                </Box>
                <Typography variant="h4" component="div">
                  {stat.value}
                </Typography>
                {stat.change && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp sx={{ fontSize: 16, color: stat.change > 0 ? 'success.main' : 'error.main' }} />
                    <Typography
                      variant="body2"
                      sx={{ ml: 0.5, color: stat.change > 0 ? 'success.main' : 'error.main' }}
                    >
                      {stat.change > 0 ? '+' : ''}{stat.change}%
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Sales Trend */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              매출 추이
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => `₩${(value as number / 1000000).toFixed(0)}M`} />
                <Legend />
                <Line type="monotone" dataKey="revenue" stroke="#8884d8" name="실적" />
                <Line type="monotone" dataKey="target" stroke="#82ca9d" name="목표" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Client Distribution */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              거래처 비중
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={clientData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {clientData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              최근 활동
            </Typography>
            <Box sx={{ mt: 2 }}>
              {[
                { text: '서울메디컬센터 방문 보고서 작성', time: '2시간 전', type: 'document' },
                { text: 'Q2 실적 분석 완료', time: '4시간 전', type: 'analytics' },
                { text: '부산클리닉 일정 확정', time: '어제', type: 'schedule' },
                { text: '규정 검토 통과', time: '어제', type: 'compliance' },
              ].map((activity, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ mr: 2 }}>
                    {activity.type === 'document' && <Description color="primary" />}
                    {activity.type === 'analytics' && <TrendingUp color="secondary" />}
                    {activity.type === 'schedule' && <ScheduleIcon color="info" />}
                    {activity.type === 'compliance' && <CheckCircle color="success" />}
                  </Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2">{activity.text}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {activity.time}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Upcoming Tasks */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              예정된 작업
            </Typography>
            <Box sx={{ mt: 2 }}>
              {[
                { task: '대구약국 제안서 제출', due: '오늘', priority: 'high' },
                { task: '월간 실적 보고', due: '내일', priority: 'medium' },
                { task: '신제품 교육 참석', due: '3일 후', priority: 'low' },
                { task: '분기 전략 회의', due: '다음 주', priority: 'medium' },
              ].map((task, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2">{task.task}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      마감: {task.due}
                    </Typography>
                  </Box>
                  <Chip
                    label={task.priority === 'high' ? '높음' : task.priority === 'medium' ? '보통' : '낮음'}
                    size="small"
                    color={task.priority === 'high' ? 'error' : task.priority === 'medium' ? 'warning' : 'default'}
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;