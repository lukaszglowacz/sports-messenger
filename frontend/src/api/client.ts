/**
 * API client for backend communication.
 * 
 * Provides typed methods for all backend endpoints.
 * Uses axios for HTTP requests.
 */

import axios from 'axios';
import type {
  User,
  Message,
  ContactListResponse,
  ContactExchange,
  MessageLimits,
  ValidationResponse,
  MessageCreateRequest,
  ContactExchangeCreateRequest,
  ContactExchangeActionRequest,
} from '../types';

// Get API base URL from environment or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * API client with typed methods for all endpoints
 */
export const apiClient = {
  // ========== User Endpoints ==========
  
  /**
   * Get all users in the system
   */
  async getUsers(): Promise<User[]> {
    const response = await api.get<User[]>('/users');
    return response.data;
  },

  /**
   * Get a specific user by ID
   */
  async getUser(userId: number): Promise<User> {
    const response = await api.get<User>(`/users/${userId}`);
    return response.data;
  },

  // ========== Contact Endpoints ==========
  
  /**
   * Get complete contact list for a user
   * 
   * @param userId - Current user ID
   * @returns Contact list with contacts, potential contacts, and pending requests
   */
  async getContacts(userId: number): Promise<ContactListResponse> {
    const response = await api.get<ContactListResponse>('/contacts', {
      params: { user_id: userId },
    });
    return response.data;
  },

  /**
   * Send a contact exchange request
   * 
   * @param request - Exchange request details
   * @returns Created contact exchange
   */
  async sendExchangeRequest(
    request: ContactExchangeCreateRequest
  ): Promise<ContactExchange> {
    const response = await api.post<ContactExchange>(
      '/contacts/exchange/request',
      request
    );
    return response.data;
  },

  /**
   * Accept a contact exchange request
   * 
   * @param exchangeId - ID of exchange to accept
   * @param userId - User accepting the request
   * @returns Updated contact exchange
   */
  async acceptExchangeRequest(
    exchangeId: number,
    userId: number
  ): Promise<ContactExchange> {
    const request: ContactExchangeActionRequest = { user_id: userId };
    const response = await api.post<ContactExchange>(
      `/contacts/exchange/${exchangeId}/accept`,
      request
    );
    return response.data;
  },

  /**
   * Reject a contact exchange request
   * 
   * @param exchangeId - ID of exchange to reject
   * @param userId - User rejecting the request
   * @returns Updated contact exchange
   */
  async rejectExchangeRequest(
    exchangeId: number,
    userId: number
  ): Promise<ContactExchange> {
    const request: ContactExchangeActionRequest = { user_id: userId };
    const response = await api.post<ContactExchange>(
      `/contacts/exchange/${exchangeId}/reject`,
      request
    );
    return response.data;
  },

  /**
   * Disconnect a contact (delete exchange)
   * 
   * @param exchangeId - ID of exchange to delete
   * @param userId - User disconnecting
   */
  async disconnectContact(
    exchangeId: number,
    userId: number
  ): Promise<void> {
    await api.delete(`/contacts/exchange/${exchangeId}`, {
      params: { user_id: userId },
    });
  },

  // ========== Message Endpoints ==========
  
  /**
   * Send a new message
   * 
   * @param message - Message details
   * @returns Created message
   * @throws Error if validation fails or limits exceeded
   */
  async sendMessage(message: MessageCreateRequest): Promise<Message> {
    const response = await api.post<Message>('/messages', message);
    return response.data;
  },

  /**
   * Get conversation history between two users
   * 
   * @param userId - Current user ID
   * @param contactId - Contact user ID
   * @returns List of messages
   */
  async getMessages(userId: number, contactId: number): Promise<Message[]> {
    const response = await api.get<Message[]>('/messages', {
      params: {
        user_id: userId,
        contact_id: contactId,
      },
    });
    return response.data;
  },

  /**
   * Get current message limits for a user
   * 
   * @param userId - User to check limits for
   * @param officialId - Optional - check limit to specific official
   * @returns Current message limits
   */
  async getMessageLimits(
    userId: number,
    officialId?: number
  ): Promise<MessageLimits> {
    const response = await api.get<MessageLimits>('/messages/limits', {
      params: {
        user_id: userId,
        official_id: officialId,
      },
    });
    return response.data;
  },

  /**
   * Validate if a message can be sent (without sending)
   * 
   * @param senderId - User who would send
   * @param recipientId - User who would receive
   * @returns Validation result
   */
  async validateMessage(
    senderId: number,
    recipientId: number
  ): Promise<ValidationResponse> {
    const response = await api.post<ValidationResponse>('/messages/validate', null, {
      params: {
        sender_id: senderId,
        recipient_id: recipientId,
      },
    });
    return response.data;
  },
};

export default apiClient;
