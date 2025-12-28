/**
 * UserSwitcher component.
 * 
 * Dropdown for switching between users (Zawodnik 1, Zawodnik 2, Manager).
 * Used for testing different user perspectives.
 */

import { FormControl, Select, MenuItem, Avatar, Box, Typography, useMediaQuery, useTheme } from '@mui/material';
import { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { useUserStore } from '../store/userStore';
import type { User, UserType } from '../types';

/**
 * Get avatar color based on user type
 */
const getUserColor = (type: UserType): string => {
  return type === 'ATHLETE' ? '#2196f3' : '#ff9800';
};

/**
 * Get icon based on user type
 */
const getUserIcon = (type: UserType): string => {
  return type === 'ATHLETE' ? '👤' : '👔';
};

export const UserSwitcher = () => {
  const [users, setUsers] = useState<User[]>([]);
  const { currentUserId, setCurrentUser } = useUserStore();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm')); // < 600px
  const isSmall = useMediaQuery(theme.breakpoints.down('md')); // < 900px

  // Fetch all users on component mount
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const allUsers = await apiClient.getUsers();
        setUsers(allUsers);
        
        // Set initial user if not set
        if (currentUserId && !useUserStore.getState().currentUser) {
          const user = allUsers.find(u => u.id === currentUserId);
          if (user) {
            setCurrentUser(currentUserId, user);
          }
        }
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    };

    fetchUsers();
  }, []);

  const handleUserChange = async (userId: number) => {
    const user = users.find(u => u.id === userId);
    if (user) {
      setCurrentUser(userId, user);
    }
  };

  return (
    <Box sx={{ minWidth: isMobile ? 120 : isSmall ? 180 : 250 }}>
      <FormControl fullWidth size="small">
        <Select
          value={currentUserId || ''}
          onChange={(e) => handleUserChange(Number(e.target.value))}
          displayEmpty
          sx={{
            '& .MuiSelect-select': {
              py: 1,
            }
          }}
          renderValue={(selected) => {
            const user = users.find(u => u.id === selected);
            if (!user) return 'Select user';
            
            return (
              <Box display="flex" alignItems="center" gap={1}>
                <Avatar
                  sx={{
                    width: isMobile ? 28 : 32,
                    height: isMobile ? 28 : 32,
                    bgcolor: getUserColor(user.type),
                    fontSize: isMobile ? '0.9rem' : '1rem'
                  }}
                >
                  {getUserIcon(user.type)}
                </Avatar>
                <Typography 
                  variant="body2" 
                  sx={{ 
                    fontSize: isMobile ? '0.75rem' : '0.875rem',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis'
                  }}
                >
                  {isMobile ? (
                    // Mobile: tylko nazwa
                    <strong>{user.name}</strong>
                  ) : (
                    // Desktop: pełny tekst
                    <>Zalogowany jako: <strong>{user.name}</strong></>
                  )}
                </Typography>
              </Box>
            );
          }}
        >
          {users.map((user) => (
            <MenuItem key={user.id} value={user.id}>
              <Box display="flex" alignItems="center" gap={1}>
                <Avatar
                  sx={{
                    width: 32,
                    height: 32,
                    bgcolor: getUserColor(user.type),
                    fontSize: '1rem'
                  }}
                >
                  {getUserIcon(user.type)}
                </Avatar>
                <Box>
                  <Typography variant="body2">{user.name}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {user.type === 'ATHLETE' ? 'Zawodnik' : 'Manager'}
                  </Typography>
                </Box>
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
};
