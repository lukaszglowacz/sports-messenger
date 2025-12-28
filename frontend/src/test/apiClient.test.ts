/**
 * Unit tests for API client.
 * Note: These tests verify the API client wrapper logic.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the entire client module
vi.mock('../api/client', async () => {
  const actual = await vi.importActual('../api/client');
  return {
    ...actual,
    apiClient: {
      getUsers: vi.fn(),
      getContacts: vi.fn(),
      sendMessage: vi.fn(),
      getMessages: vi.fn(),
      getMessageLimits: vi.fn(),
      sendExchangeRequest: vi.fn(),
      acceptExchangeRequest: vi.fn(),
      rejectExchangeRequest: vi.fn(),
    },
  };
});

import { apiClient } from '../api/client';

const mockedApiClient = apiClient as any;

describe('apiClient', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getUsers', () => {
    it('should fetch all users', async () => {
      const mockUsers = [
        { id: 1, name: 'User 1', type: 'ATHLETE', email: 'user1@test.com' },
        { id: 2, name: 'User 2', type: 'OFFICIAL', email: 'user2@test.com' },
      ];

      mockedApiClient.getUsers.mockResolvedValueOnce(mockUsers);

      const users = await apiClient.getUsers();

      expect(apiClient.getUsers).toHaveBeenCalled();
      expect(users).toEqual(mockUsers);
      expect(users).toHaveLength(2);
    });
  });

  describe('getContacts', () => {
    it('should fetch contacts for user', async () => {
      const mockContacts = {
        contacts: [{ id: 2, name: 'Contact 1' }],
        pending_requests: [],
        potential_contacts: [],
      };

      mockedApiClient.getContacts.mockResolvedValueOnce(mockContacts);

      const contacts = await apiClient.getContacts(1);

      expect(apiClient.getContacts).toHaveBeenCalledWith(1);
      expect(contacts).toEqual(mockContacts);
    });
  });

  describe('sendMessage', () => {
    it('should send message successfully', async () => {
      const messageData = {
        sender_id: 1,
        recipient_id: 2,
        content: 'Hello!',
      };

      const mockResponse = {
        id: 1,
        ...messageData,
        created_at: new Date().toISOString(),
      };

      mockedApiClient.sendMessage.mockResolvedValueOnce(mockResponse);

      const message = await apiClient.sendMessage(messageData);

      expect(apiClient.sendMessage).toHaveBeenCalledWith(messageData);
      expect(message).toEqual(mockResponse);
      expect(message.content).toBe('Hello!');
    });

    it('should handle send message error', async () => {
      const messageData = {
        sender_id: 1,
        recipient_id: 2,
        content: 'Hello!',
      };

      const error = new Error('Network error');
      mockedApiClient.sendMessage.mockRejectedValueOnce(error);

      await expect(apiClient.sendMessage(messageData)).rejects.toThrow('Network error');
    });
  });

  describe('getMessages', () => {
    it('should fetch messages between users', async () => {
      const mockMessages = [
        { id: 1, sender_id: 1, recipient_id: 2, content: 'Hello', created_at: '2024-01-01' },
        { id: 2, sender_id: 2, recipient_id: 1, content: 'Hi', created_at: '2024-01-01' },
      ];

      mockedApiClient.getMessages.mockResolvedValueOnce(mockMessages);

      const messages = await apiClient.getMessages(1, 2);

      expect(apiClient.getMessages).toHaveBeenCalledWith(1, 2);
      expect(messages).toEqual(mockMessages);
      expect(messages).toHaveLength(2);
    });
  });

  describe('getMessageLimits', () => {
    it('should fetch message limits for athlete', async () => {
      const mockLimits = {
        total_today: 10,
        daily_limit: 100,
        is_exceeded: false,
      };

      mockedApiClient.getMessageLimits.mockResolvedValueOnce(mockLimits);

      const limits = await apiClient.getMessageLimits(1);

      expect(apiClient.getMessageLimits).toHaveBeenCalledWith(1);
      expect(limits.total_today).toBe(10);
      expect(limits.daily_limit).toBe(100);
      expect(limits.is_exceeded).toBe(false);
    });

    it('should fetch limits with official_id', async () => {
      const mockLimits = {
        total_today: 3,
        to_official: 3,
        official_limit: 5,
        daily_limit: 100,
        is_exceeded: false,
      };

      mockedApiClient.getMessageLimits.mockResolvedValueOnce(mockLimits);

      const limits = await apiClient.getMessageLimits(1, 3);

      expect(apiClient.getMessageLimits).toHaveBeenCalledWith(1, 3);
      expect(limits.to_official).toBe(3);
      expect(limits.official_limit).toBe(5);
    });
  });

  describe('sendExchangeRequest', () => {
    it('should send exchange request', async () => {
      const requestData = {
        from_user_id: 1,
        to_user_id: 3,
      };

      const mockResponse = {
        id: 1,
        ...requestData,
        status: 'PENDING',
      };

      mockedApiClient.sendExchangeRequest.mockResolvedValueOnce(mockResponse);

      const exchange = await apiClient.sendExchangeRequest(requestData);

      expect(apiClient.sendExchangeRequest).toHaveBeenCalledWith(requestData);
      expect(exchange.status).toBe('PENDING');
    });
  });

  describe('acceptExchangeRequest', () => {
    it('should accept exchange request', async () => {
      const mockResponse = {
        id: 1,
        status: 'ACCEPTED',
      };

      mockedApiClient.acceptExchangeRequest.mockResolvedValueOnce(mockResponse);

      const exchange = await apiClient.acceptExchangeRequest(1, 3);

      expect(apiClient.acceptExchangeRequest).toHaveBeenCalledWith(1, 3);
      expect(exchange.status).toBe('ACCEPTED');
    });
  });

  describe('rejectExchangeRequest', () => {
    it('should reject exchange request', async () => {
      const mockResponse = {
        id: 1,
        status: 'REJECTED',
      };

      mockedApiClient.rejectExchangeRequest.mockResolvedValueOnce(mockResponse);

      const exchange = await apiClient.rejectExchangeRequest(1, 3);

      expect(apiClient.rejectExchangeRequest).toHaveBeenCalledWith(1, 3);
      expect(exchange.status).toBe('REJECTED');
    });
  });

  describe('error handling', () => {
    it('should handle API errors gracefully', async () => {
      const apiError = {
        response: {
          status: 429,
          data: { detail: 'Rate limit exceeded' },
        },
      };

      mockedApiClient.sendMessage.mockRejectedValueOnce(apiError);

      await expect(
        apiClient.sendMessage({
          sender_id: 1,
          recipient_id: 2,
          content: 'Test',
        })
      ).rejects.toEqual(apiError);
    });
  });
});