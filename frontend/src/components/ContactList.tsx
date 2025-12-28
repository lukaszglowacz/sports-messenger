/**
 * ContactList component - Enhanced with modern design.
 * 
 * Features:
 * - Beautiful cards for contacts
 * - Better visual hierarchy
 * - Smooth transitions
 * - Improved mobile layout
 */

import { useEffect, useState } from 'react';
import {
  Box,
  List,
  ListItemButton,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Typography,
  Chip,
  Button,
  Card,
  CardContent,
  Divider,
  CircularProgress,
  Badge,
  alpha,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PendingIcon from '@mui/icons-material/Pending';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import { apiClient } from '../api/client';
import { useUserStore } from '../store/userStore';
import type { ContactListResponse, ContactInfo, PendingRequestInfo } from '../types';
import { toast } from 'react-toastify';

export const ContactList = () => {
  const { currentUserId, selectedContact, setSelectedContact, refreshTrigger } = useUserStore();
  const [contactData, setContactData] = useState<ContactListResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch contacts when user changes or refresh triggered
  useEffect(() => {
    if (!currentUserId) return;

    const fetchContacts = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getContacts(currentUserId);
        setContactData(data);
      } catch (error) {
        console.error('Failed to fetch contacts:', error);
        toast.error('Nie udało się pobrać kontaktów');
      } finally {
        setLoading(false);
      }
    };

    fetchContacts();
  }, [currentUserId, refreshTrigger]);

  const handleAcceptRequest = async (exchangeId: number) => {
    if (!currentUserId) return;
    
    try {
      await apiClient.acceptExchangeRequest(exchangeId, currentUserId);
      toast.success('✓ Zaproszenie zaakceptowane!');
      useUserStore.getState().triggerRefresh();
    } catch (error) {
      console.error('Failed to accept request:', error);
      toast.error('Nie udało się zaakceptować zaproszenia');
    }
  };

  const handleRejectRequest = async (exchangeId: number) => {
    if (!currentUserId) return;
    
    try {
      await apiClient.rejectExchangeRequest(exchangeId, currentUserId);
      toast.success('Zaproszenie odrzucone');
      useUserStore.getState().triggerRefresh();
    } catch (error) {
      console.error('Failed to reject request:', error);
      toast.error('Nie udało się odrzucić zaproszenia');
    }
  };

  const handleSendRequest = async (toUserId: number) => {
    if (!currentUserId) return;
    
    try {
      await apiClient.sendExchangeRequest({
        from_user_id: currentUserId,
        to_user_id: toUserId
      });
      toast.success('✓ Zaproszenie wysłane!');
      useUserStore.getState().triggerRefresh();
    } catch (error) {
      console.error('Failed to send request:', error);
      toast.error('Nie udało się wysłać zaproszenia');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (!contactData) {
    return (
      <Box p={2}>
        <Typography>Nie znaleziono kontaktów</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100%', overflow: 'auto', bgcolor: 'background.paper' }}>
      {/* Pending Requests Section */}
      {contactData.pending_requests.length > 0 && (
        <Box sx={{ p: 2, bgcolor: alpha('#ff9800', 0.08) }}>
          <Typography 
            variant="subtitle2" 
            fontWeight="600" 
            gutterBottom
            sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: 1,
              color: 'warning.dark'
            }}
          >
            <PendingIcon fontSize="small" />
            Oczekujące zaproszenia ({contactData.pending_requests.length})
          </Typography>
          {contactData.pending_requests.map((request: PendingRequestInfo) => (
            <Card 
              key={request.exchange_id} 
              sx={{ 
                mb: 1,
                borderLeft: 3,
                borderColor: 'warning.main',
                '&:hover': {
                  boxShadow: 3,
                }
              }}
            >
              <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Avatar sx={{ bgcolor: 'warning.main', width: 36, height: 36 }}>
                    {request.from_user.name[0]}
                  </Avatar>
                  <Box flex={1}>
                    <Typography variant="body2" fontWeight="600">
                      {request.from_user.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      wysłał/a zaproszenie
                    </Typography>
                  </Box>
                </Box>
                <Box display="flex" gap={1}>
                  <Button
                    size="small"
                    variant="contained"
                    color="success"
                    onClick={() => handleAcceptRequest(request.exchange_id)}
                    fullWidth
                    sx={{ borderRadius: 2 }}
                  >
                    Akceptuj
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    color="error"
                    onClick={() => handleRejectRequest(request.exchange_id)}
                    fullWidth
                    sx={{ borderRadius: 2 }}
                  >
                    Odrzuć
                  </Button>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}

      {/* Active Contacts */}
      <Box sx={{ p: 2 }}>
        <Typography 
          variant="subtitle2" 
          fontWeight="600" 
          gutterBottom
          sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 1,
            color: 'primary.dark'
          }}
        >
          💬 Moje kontakty ({contactData.contacts.length})
        </Typography>
        <List sx={{ p: 0 }}>
          {contactData.contacts.map((contact: ContactInfo) => (
            <ListItemButton
              key={contact.id}
              selected={selectedContact?.id === contact.id}
              onClick={() => setSelectedContact(contact)}
              sx={{
                borderRadius: 2,
                mb: 0.5,
                transition: 'all 0.2s',
                '&:hover': { 
                  bgcolor: alpha('#1976d2', 0.08),
                  transform: 'translateX(4px)',
                },
                '&.Mui-selected': {
                  bgcolor: alpha('#1976d2', 0.12),
                  borderLeft: 3,
                  borderColor: 'primary.main',
                  '&:hover': {
                    bgcolor: alpha('#1976d2', 0.16),
                  },
                },
              }}
            >
              <ListItemAvatar>
                <Badge
                  overlap="circular"
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  variant={contact.unread_count > 0 ? 'dot' : 'standard'}
                  color="error"
                >
                  <Avatar sx={{ bgcolor: 'primary.main' }}>
                    {contact.name[0]}
                  </Avatar>
                </Badge>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="body2" fontWeight="600">
                      {contact.name}
                    </Typography>
                    {contact.exchange_status === 'ACCEPTED' && (
                      <CheckCircleIcon 
                        fontSize="small" 
                        sx={{ color: 'success.main', fontSize: 16 }} 
                      />
                    )}
                    {contact.unread_count > 0 && (
                      <Chip 
                        label={contact.unread_count} 
                        size="small" 
                        color="error"
                        sx={{ height: 18, minWidth: 18, fontSize: '0.7rem' }}
                      />
                    )}
                  </Box>
                }
                secondary={
                  <Typography 
                    variant="caption" 
                    color="text.secondary"
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 1,
                      WebkitBoxOrient: 'vertical',
                    }}
                  >
                    {contact.last_message || 'Brak wiadomości'}
                  </Typography>
                }
              />
            </ListItemButton>
          ))}
        </List>
      </Box>

      {/* Potential Contacts */}
      {contactData.potential_contacts.length > 0 && (
        <>
          <Divider />
          <Box sx={{ p: 2, bgcolor: alpha('#f5f5f5', 0.5) }}>
            <Typography 
              variant="subtitle2" 
              fontWeight="600" 
              gutterBottom
              sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                color: 'text.secondary'
              }}
            >
              <PersonAddIcon fontSize="small" />
              Dostępni do wymiany ({contactData.potential_contacts.length})
            </Typography>
            <List sx={{ p: 0 }}>
              {contactData.potential_contacts.map((contact: ContactInfo) => (
                <ListItemButton
                  key={contact.id}
                  sx={{
                    borderRadius: 2,
                    mb: 0.5,
                    border: 1,
                    borderColor: 'divider',
                    '&:hover': { 
                      bgcolor: 'grey.50',
                      borderColor: 'primary.main',
                    },
                  }}
                >
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'grey.400' }}>
                      {contact.name[0]}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Typography variant="body2" fontWeight="600">
                        {contact.name}
                      </Typography>
                    }
                    secondary={
                      contact.can_send_request ? (
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => handleSendRequest(contact.id)}
                          sx={{ 
                            mt: 0.5,
                            borderRadius: 2,
                            textTransform: 'none'
                          }}
                        >
                          Wyślij zaproszenie
                        </Button>
                      ) : (
                        <Chip 
                          label="Oczekuje" 
                          size="small" 
                          color="warning"
                          sx={{ mt: 0.5 }}
                        />
                      )
                    }
                  />
                </ListItemButton>
              ))}
            </List>
          </Box>
        </>
      )}
    </Box>
  );
};
