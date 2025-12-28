/**
 * ChatWindow component - Enhanced with modern design and responsiveness.
 * 
 * Features:
 * - Beautiful message bubbles with gradients
 * - Responsive layout
 * - Better limit indicators with progress bars
 * - Smooth animations
 * - Mobile-optimized
 */

import { useEffect, useState, useRef } from 'react';
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
  Avatar,
  Alert,
  CircularProgress,
  Chip,
  LinearProgress,
  Fade,
  Tooltip,
  useMediaQuery,
  useTheme,
  Popover,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Divider
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import EmojiEmotionsIcon from '@mui/icons-material/EmojiEmotions';
import EmojiPicker, { EmojiClickData } from 'emoji-picker-react';
import { apiClient } from '../api/client';
import { useUserStore } from '../store/userStore';
import type { Message, MessageLimits } from '../types';
import { toast } from 'react-toastify';
import { formatDistanceToNow } from 'date-fns';
import { pl } from 'date-fns/locale';

export const ChatWindow = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { currentUserId, selectedContact, messages, setMessages, addMessage, setSelectedContact } = useUserStore();
  const [newMessage, setNewMessage] = useState('');
  const [limits, setLimits] = useState<MessageLimits | null>(null);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [emojiAnchor, setEmojiAnchor] = useState<null | HTMLElement>(null);
  const [infoDialogOpen, setInfoDialogOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch messages when contact selected
  useEffect(() => {
    if (!currentUserId || !selectedContact) {
      setMessages([]);
      return;
    }

    const fetchMessages = async () => {
      try {
        setLoading(true);
        const msgs = await apiClient.getMessages(currentUserId, selectedContact.id);
        setMessages(msgs);
      } catch (error) {
        console.error('Failed to fetch messages:', error);
        toast.error('Nie udało się pobrać wiadomości');
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, [currentUserId, selectedContact]);

  // Fetch limits when contact selected
  useEffect(() => {
    if (!currentUserId || !selectedContact) return;

    const fetchLimits = async () => {
      try {
        const officialId = selectedContact.type === 'OFFICIAL' ? selectedContact.id : undefined;
        const limitsData = await apiClient.getMessageLimits(currentUserId, officialId);
        setLimits(limitsData);
      } catch (error) {
        console.error('Failed to fetch limits:', error);
      }
    };

    fetchLimits();
  }, [currentUserId, selectedContact, messages.length]);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!currentUserId || !selectedContact || !newMessage.trim()) return;

    try {
      setSending(true);
      const message = await apiClient.sendMessage({
        sender_id: currentUserId,
        recipient_id: selectedContact.id,
        content: newMessage.trim()
      });
      
      addMessage(message);
      setNewMessage('');
      toast.success('✓ Wysłano');
    } catch (error: any) {
      console.error('Failed to send message:', error);
      
      // Handle specific error codes
      if (error.response?.status === 429) {
        // Too Many Requests - limit exceeded
        const detail = error.response?.data?.detail || 'Osiągnięto limit wiadomości';
        toast.error(`⛔ ${detail}`, { autoClose: 5000 });
      } else if (error.response?.status === 400) {
        // Bad Request - validation error
        const detail = error.response?.data?.detail || 'Nieprawidłowe dane';
        toast.error(detail);
      } else {
        // Generic error
        const errorMessage = error.response?.data?.detail || 'Nie udało się wysłać wiadomości';
        toast.error(errorMessage);
      }
      
      // Refresh limits to show updated state
      if (currentUserId && selectedContact) {
        const officialId = selectedContact.type === 'OFFICIAL' ? selectedContact.id : undefined;
        const limitsData = await apiClient.getMessageLimits(currentUserId, officialId);
        setLimits(limitsData);
      }
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleBack = () => {
    setSelectedContact(null);
  };

  const handleEmojiClick = (emojiData: EmojiClickData) => {
    setNewMessage(prev => prev + emojiData.emoji);
  };

  const handleEmojiOpen = (event: React.MouseEvent<HTMLElement>) => {
    setEmojiAnchor(event.currentTarget);
  };

  const handleEmojiClose = () => {
    setEmojiAnchor(null);
  };

  // Calculate progress for limits
  const getProgress = (current: number, max: number) => {
    return (current / max) * 100;
  };

  const getLimitColor = (current: number, max: number) => {
    const percentage = (current / max) * 100;
    if (percentage >= 90) return 'error';
    if (percentage >= 70) return 'warning';
    return 'success';
  };

  if (!selectedContact) {
    return (
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        height="100%"
        sx={{
          background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        }}
      >
        <Box textAlign="center" sx={{ opacity: 0.6 }}>
          <Typography variant="h4" gutterBottom>
            💬
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Wybierz kontakt
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Kliknij na kontakt aby rozpocząć rozmowę
          </Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box display="flex" flexDirection="column" height="100%" sx={{ bgcolor: '#f5f7fa' }}>
      {/* Enhanced Header */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          borderRadius: 0,
          borderBottom: 1,
          borderColor: 'divider',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
        }}
      >
        {isMobile && (
          <IconButton color="inherit" onClick={handleBack} size="small">
            <ArrowBackIcon />
          </IconButton>
        )}
        
        <Avatar 
          sx={{ 
            width: 48, 
            height: 48,
            bgcolor: 'rgba(255,255,255,0.2)',
            border: '2px solid rgba(255,255,255,0.3)',
            fontSize: '1.5rem'
          }}
        >
          {selectedContact.name[0]}
        </Avatar>
        
        <Box flex={1}>
          <Typography variant="h6" fontWeight="bold">
            {selectedContact.name}
          </Typography>
          {selectedContact.exchange_status === 'ACCEPTED' && (
            <Chip 
              label="✓ Połączeni" 
              size="small" 
              sx={{ 
                height: 20,
                bgcolor: 'rgba(76, 175, 80, 0.2)',
                color: 'white',
                fontSize: '0.7rem',
                border: '1px solid rgba(255,255,255,0.3)'
              }} 
            />
          )}
        </Box>

        {limits && (
          <Tooltip title="Informacje o limitach">
            <IconButton 
              color="inherit" 
              size="small"
              onClick={() => setInfoDialogOpen(true)}
            >
              <InfoOutlinedIcon />
            </IconButton>
          </Tooltip>
        )}
      </Paper>

      {/* Messages Area */}
      <Box
        flex={1}
        sx={{
          overflow: 'auto',
          p: { xs: 1, sm: 2 },
          background: 'linear-gradient(to bottom, #f5f7fa 0%, #ffffff 100%)',
        }}
      >
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="100%">
            <CircularProgress />
          </Box>
        ) : messages.length === 0 ? (
          <Box 
            display="flex" 
            alignItems="center" 
            justifyContent="center" 
            height="100%"
            sx={{ opacity: 0.5 }}
          >
            <Typography color="text.secondary" align="center">
              Brak wiadomości.<br />Rozpocznij rozmowę! 👋
            </Typography>
          </Box>
        ) : (
          <Box>
            {messages.map((message: Message, index) => {
              const isOwn = message.sender_id === currentUserId;
              const showAvatar = index === 0 || messages[index - 1].sender_id !== message.sender_id;
              
              return (
                <Fade in key={message.id} timeout={300}>
                  <Box
                    display="flex"
                    justifyContent={isOwn ? 'flex-end' : 'flex-start'}
                    mb={1.5}
                    sx={{
                      animation: 'slideIn 0.3s ease-out',
                      '@keyframes slideIn': {
                        from: { opacity: 0, transform: 'translateY(10px)' },
                        to: { opacity: 1, transform: 'translateY(0)' }
                      }
                    }}
                  >
                    {!isOwn && showAvatar && (
                      <Avatar 
                        sx={{ 
                          width: 32, 
                          height: 32, 
                          mr: 1,
                          bgcolor: 'primary.main' 
                        }}
                      >
                        {selectedContact.name[0]}
                      </Avatar>
                    )}
                    {!isOwn && !showAvatar && <Box sx={{ width: 40 }} />}
                    
                    <Paper
                      elevation={isOwn ? 2 : 1}
                      sx={{
                        p: 1.5,
                        maxWidth: { xs: '85%', sm: '70%' },
                        background: isOwn 
                          ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                          : 'white',
                        color: isOwn ? 'white' : 'text.primary',
                        borderRadius: 2,
                        borderTopRightRadius: isOwn ? 4 : 16,
                        borderTopLeftRadius: isOwn ? 16 : 4,
                        wordBreak: 'break-word',
                      }}
                    >
                      <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                        {message.content}
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{
                          opacity: 0.7,
                          display: 'block',
                          mt: 0.5,
                          fontSize: '0.7rem'
                        }}
                      >
                        {formatDistanceToNow(new Date(message.created_at), {
                          addSuffix: true,
                          locale: pl
                        })}
                      </Typography>
                    </Paper>
                  </Box>
                </Fade>
              );
            })}
            <div ref={messagesEndRef} />
          </Box>
        )}
      </Box>

      {/* Enhanced Limits Display */}
      {limits && limits.daily_limit && (
        <Box
          sx={{
            px: 2,
            py: 1.5,
            bgcolor: limits.is_exceeded ? '#ffebee' : 'background.paper',
            borderTop: 1,
            borderColor: 'divider',
          }}
        >
          {limits.is_exceeded && (
            <Alert severity="error" sx={{ mb: 1, py: 0 }}>
              <Typography variant="caption" fontWeight="600">
                ⛔ Osiągnięto limit wiadomości!
              </Typography>
            </Alert>
          )}
          
          {/* Limit for specific official (ONLY if talking to OFFICIAL and limit exists) */}
          {selectedContact.type === 'OFFICIAL' && limits.official_limit && limits.to_official !== undefined && (
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <Typography
                variant="caption"
                fontWeight="600"
                color={
                  (limits.to_official || 0) >= limits.official_limit
                    ? 'error.main'
                    : 'text.secondary'
                }
              >
                Do {selectedContact.name}: {limits.to_official || 0}/{limits.official_limit}
              </Typography>
              <Box flex={1}>
                <LinearProgress 
                  variant="determinate" 
                  value={getProgress(limits.to_official || 0, limits.official_limit)}
                  color={getLimitColor(limits.to_official || 0, limits.official_limit)}
                  sx={{ height: 6, borderRadius: 3 }}
                />
              </Box>
            </Box>
          )}
          
          {/* Daily total limit (always shown for athletes) */}
          <Box display="flex" alignItems="center" gap={1}>
            <Typography
              variant="caption"
              fontWeight="600"
              color="text.secondary"
            >
              Ogólnie dzisiaj: {limits.total_today}/{limits.daily_limit}
            </Typography>
            <Box flex={1}>
              <LinearProgress 
                variant="determinate" 
                value={getProgress(limits.total_today, limits.daily_limit)}
                color={getLimitColor(limits.total_today, limits.daily_limit)}
                sx={{ height: 6, borderRadius: 3 }}
              />
            </Box>
          </Box>
        </Box>
      )}

      {/* Enhanced Input */}
      {selectedContact.can_message ? (
        <Paper
          elevation={3}
          sx={{
            p: { xs: 1.5, sm: 2 },
            display: 'flex',
            gap: 1,
            borderRadius: 0,
            bgcolor: 'background.paper',
            borderTop: 1,
            borderColor: 'divider',
          }}
        >
          <TextField
            fullWidth
            placeholder="Napisz wiadomość..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={sending || limits?.is_exceeded}
            multiline
            maxRows={4}
            size="small"
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 3,
                bgcolor: 'grey.50',
                '&:hover': {
                  bgcolor: 'grey.100',
                },
                '& fieldset': {
                  borderColor: 'transparent',
                },
                '&:hover fieldset': {
                  borderColor: 'primary.main',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'primary.main',
                },
              },
            }}
          />
          
          {/* Emoji Picker Button */}
          <Tooltip title="Dodaj emoji">
            <IconButton
              onClick={handleEmojiOpen}
              disabled={sending || limits?.is_exceeded}
              sx={{
                color: 'primary.main',
                '&:hover': {
                  bgcolor: 'primary.light',
                  color: 'white',
                },
              }}
            >
              <EmojiEmotionsIcon />
            </IconButton>
          </Tooltip>

          {/* Emoji Picker Popover */}
          <Popover
            open={Boolean(emojiAnchor)}
            anchorEl={emojiAnchor}
            onClose={handleEmojiClose}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            transformOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
          >
            <EmojiPicker
              onEmojiClick={handleEmojiClick}
              width={isMobile ? 280 : 350}
              height={400}
            />
          </Popover>
          
          <IconButton
            color="primary"
            onClick={handleSendMessage}
            disabled={!newMessage.trim() || sending || limits?.is_exceeded}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              '&:hover': {
                background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
              },
              '&.Mui-disabled': {
                bgcolor: 'grey.300',
                color: 'grey.500',
              },
              width: 48,
              height: 48,
            }}
          >
            {sending ? <CircularProgress size={24} color="inherit" /> : <SendIcon />}
          </IconButton>
        </Paper>
      ) : (
        <Alert severity="warning" sx={{ m: 2, borderRadius: 2 }}>
          <strong>Wymiana kontaktów wymagana</strong>
          <br />
          Musisz wymienić kontakty z tym użytkownikiem, aby wysyłać wiadomości.
        </Alert>
      )}

      {/* Info Dialog - Limits Information */}
      <Dialog
        open={infoDialogOpen}
        onClose={() => setInfoDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle sx={{ bgcolor: 'primary.main', color: 'white' }}>
          📊 Informacje o limitach wiadomości
        </DialogTitle>
        <DialogContent sx={{ mt: 2 }}>
          {limits ? (
            <Box>
              {/* Daily limit info */}
              {limits.daily_limit && (
                <Box mb={3}>
                  <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                    🗓️ Dzienny limit ogólny
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Maksymalna liczba wiadomości na dzień do wszystkich użytkowników
                  </Typography>
                  <Box display="flex" alignItems="center" gap={2} mt={1}>
                    <LinearProgress
                      variant="determinate"
                      value={getProgress(limits.total_today, limits.daily_limit)}
                      color={getLimitColor(limits.total_today, limits.daily_limit)}
                      sx={{ flex: 1, height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="h6" fontWeight="600">
                      {limits.total_today}/{limits.daily_limit}
                    </Typography>
                  </Box>
                </Box>
              )}

              <Divider />

              {/* Official limit info */}
              {selectedContact.type === 'OFFICIAL' && limits.official_limit && (
                <Box mt={3}>
                  <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                    👤 Limit do {selectedContact.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Maksymalna liczba wiadomości na dzień do tego działacza
                  </Typography>
                  <Box display="flex" alignItems="center" gap={2} mt={1}>
                    <LinearProgress
                      variant="determinate"
                      value={getProgress(limits.to_official || 0, limits.official_limit)}
                      color={getLimitColor(limits.to_official || 0, limits.official_limit)}
                      sx={{ flex: 1, height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="h6" fontWeight="600">
                      {limits.to_official || 0}/{limits.official_limit}
                    </Typography>
                  </Box>
                </Box>
              )}

              {/* Rules info */}
              <Box mt={3} p={2} bgcolor="grey.50" borderRadius={2}>
                <Typography variant="subtitle2" fontWeight="600" gutterBottom>
                  📋 Zasady:
                </Typography>
                <Typography variant="body2" component="ul" sx={{ pl: 2, mb: 0 }}>
                  <li>Zawodnicy mogą wysyłać <strong>max 100 wiadomości/dzień</strong> do wszystkich</li>
                  <li>Do działaczy <strong>max 5 wiadomości/dzień</strong> na osobę</li>
                  <li>Limity resetują się o <strong>północy</strong></li>
                </Typography>
              </Box>

              {/* Warning if limit exceeded */}
              {limits.is_exceeded && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  <strong>⛔ Osiągnięto limit!</strong><br />
                  Nie możesz wysyłać więcej wiadomości do tego użytkownika dzisiaj.
                </Alert>
              )}
            </Box>
          ) : (
            <Typography color="text.secondary">
              Brak informacji o limitach
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setInfoDialogOpen(false)} variant="contained">
            Zamknij
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
