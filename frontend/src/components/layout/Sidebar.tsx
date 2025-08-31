import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Box,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Dashboard,
  Analytics,
  People,
  Description,
  Schedule,
  VerifiedUser,
  AutoAwesome,
} from '@mui/icons-material';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const menuItems = [
  { path: '/dashboard', label: '대시보드', icon: Dashboard },
  { path: '/analytics', label: '실적 분석', icon: Analytics },
  { path: '/clients', label: '거래처 관리', icon: People },
  { path: '/documents', label: '문서 관리', icon: Description },
  { path: '/schedule', label: '일정 관리', icon: Schedule },
  { path: '/compliance', label: '규정 검토', icon: VerifiedUser },
];

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleNavigate = (path: string) => {
    navigate(path);
    if (isMobile) {
      onClose();
    }
  };

  const drawerContent = (
    <Box>
      <Toolbar />
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <ListItem key={item.path} disablePadding>
                <ListItemButton
                  onClick={() => handleNavigate(item.path)}
                  selected={isActive}
                  sx={{
                    '&.Mui-selected': {
                      backgroundColor: 'primary.main',
                      color: 'white',
                      '&:hover': {
                        backgroundColor: 'primary.dark',
                      },
                      '& .MuiListItemIcon-root': {
                        color: 'white',
                      },
                    },
                  }}
                >
                  <ListItemIcon>
                    <Icon />
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>

        <Box sx={{ p: 2, mt: 2 }}>
          <ListItemButton
            sx={{
              backgroundColor: 'secondary.main',
              color: 'white',
              borderRadius: 2,
              '&:hover': {
                backgroundColor: 'secondary.dark',
              },
            }}
            onClick={() => handleNavigate('/workflow')}
          >
            <ListItemIcon>
              <AutoAwesome sx={{ color: 'white' }} />
            </ListItemIcon>
            <ListItemText primary="AI 워크플로우" />
          </ListItemButton>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Drawer
      variant={isMobile ? 'temporary' : 'persistent'}
      open={open}
      onClose={onClose}
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;