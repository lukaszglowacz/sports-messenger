/**
 * Main App component - Enhanced with responsiveness and better design.
 * 
 * Features:
 * - Responsive layout (mobile, tablet, desktop)
 * - Modern gradient theme
 * - Smooth transitions
 * - Mobile-first approach
 */

import { useState } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  CssBaseline, 
  ThemeProvider, 
  createTheme,
  IconButton,
  useMediaQuery,
  Drawer
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { UserSwitcher } from './components/UserSwitcher';
import { ContactList } from './components/ContactList';
import { ChatWindow } from './components/ChatWindow';
import { useUserStore } from './store/userStore';

// Enhanced theme with gradients and modern colors
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#ff9800',
      light: '#ffb74d',
      dark: '#f57c00',
    },
    background: {
      default: '#f5f7fa',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h5: {
      fontWeight: 700,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

function App() {
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const { selectedContact } = useUserStore();
  
  // Check if mobile (less than 900px)
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // On mobile, show chat if contact selected, otherwise show contact list
  const showChatOnMobile = isMobile && selectedContact;

  const handleDrawerToggle = () => {
    setMobileDrawerOpen(!mobileDrawerOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box 
        sx={{ 
          height: '100vh', 
          display: 'flex', 
          flexDirection: 'column',
          bgcolor: 'background.default'
        }}
      >
        {/* Header with gradient */}
        <Paper
          elevation={0}
          sx={{
            background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
            color: 'white',
            p: { xs: 1, sm: 2 },
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderRadius: 0,
            zIndex: 1100,
            boxShadow: '0 2px 8px rgba(25, 118, 210, 0.25)',
            gap: { xs: 0.5, sm: 2 }
          }}
        >
          <Box display="flex" alignItems="center" gap={1}>
            {isMobile && showChatOnMobile && (
              <IconButton 
                color="inherit" 
                onClick={handleDrawerToggle}
                sx={{ mr: { xs: 0, sm: 1 }, p: { xs: 0.5, sm: 1 } }}
                size="small"
              >
                <MenuIcon />
              </IconButton>
            )}
            <Typography 
              variant={isMobile ? 'h6' : 'h5'} 
              component="h1" 
              fontWeight="bold"
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 1,
                fontSize: { xs: '1rem', sm: '1.25rem', md: '1.5rem' }
              }}
            >
              <span style={{ fontSize: isMobile ? '1.2rem' : '2rem' }}>⚽</span>
              <span style={{ display: isMobile ? 'none' : 'inline' }}>Sports Messenger</span>
              <span style={{ display: isMobile ? 'inline' : 'none' }}>Messenger</span>
            </Typography>
          </Box>
          <UserSwitcher />
        </Paper>

        {/* Main Content - Responsive */}
        <Box sx={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
          {/* Desktop: Side-by-side layout */}
          {!isMobile && (
            <>
              {/* Contact List - Left Panel */}
              <Paper
                elevation={0}
                sx={{
                  width: 380,
                  borderRadius: 0,
                  borderRight: 1,
                  borderColor: 'divider',
                  overflow: 'auto',
                  bgcolor: 'background.paper'
                }}
              >
                <ContactList />
              </Paper>

              {/* Chat Window - Right Panel */}
              <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <ChatWindow />
              </Box>
            </>
          )}

          {/* Mobile: Stack layout with drawer */}
          {isMobile && (
            <>
              {/* Mobile Drawer for Contact List */}
              <Drawer
                anchor="left"
                open={mobileDrawerOpen}
                onClose={handleDrawerToggle}
                sx={{
                  '& .MuiDrawer-paper': {
                    width: '85%',
                    maxWidth: 360,
                  },
                }}
              >
                <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="h6" fontWeight="bold">
                      Kontakty
                    </Typography>
                    <IconButton onClick={handleDrawerToggle}>
                      <CloseIcon />
                    </IconButton>
                  </Box>
                </Box>
                <ContactList />
              </Drawer>

              {/* Mobile Main View */}
              {showChatOnMobile ? (
                // Show chat when contact selected
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                  <ChatWindow />
                </Box>
              ) : (
                // Show contact list when no contact selected
                <Box sx={{ flex: 1, overflow: 'auto' }}>
                  <ContactList />
                </Box>
              )}
            </>
          )}
        </Box>
      </Box>

      {/* Toast Notifications - Positioned for mobile */}
      <ToastContainer
        position={isMobile ? 'top-center' : 'bottom-right'}
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        pauseOnFocusLoss
        draggable
        pauseOnHover
        style={{ zIndex: 9999 }}
      />
    </ThemeProvider>
  );
}

export default App;
