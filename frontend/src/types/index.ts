/**
 * TypeScript type definitions for the application.
 * 
 * These types match the Pydantic schemas from backend API.
 */

/**
 * User type enum
 */
export enum UserType {
  ATHLETE = 'ATHLETE',
  OFFICIAL = 'OFFICIAL',
}

/**
 * Contact exchange status enum
 */
export enum ContactExchangeStatus {
  PENDING = 'PENDING',
  ACCEPTED = 'ACCEPTED',
  REJECTED = 'REJECTED',
}

/**
 * User model
 */
export interface User {
  id: number;
  name: string;
  email: string;
  type: UserType;
  created_at: string;
}

/**
 * Message model
 */
export interface Message {
  id: number;
  sender_id: number;
  recipient_id: number;
  content: string;
  created_at: string;
  read: boolean;
}

/**
 * Contact exchange model
 */
export interface ContactExchange {
  id: number;
  athlete_id: number;
  official_id: number;
  status: ContactExchangeStatus;
  initiated_by: number;
  created_at: string;
  responded_at: string | null;
}

/**
 * Contact info with additional metadata
 */
export interface ContactInfo {
  id: number;
  name: string;
  type: UserType;
  exchange_status: ContactExchangeStatus | null;
  exchange_id: number | null;
  can_message: boolean;
  can_send_request: boolean;
  last_message: string | null;
  last_message_time: string | null;
  unread_count: number;
}

/**
 * Pending contact exchange request info
 */
export interface PendingRequestInfo {
  exchange_id: number;
  from_user: User;
  to_user: User;
  status: ContactExchangeStatus;
  created_at: string;
}

/**
 * Complete contact list response
 */
export interface ContactListResponse {
  contacts: ContactInfo[];
  potential_contacts: ContactInfo[];
  pending_requests: PendingRequestInfo[];
}

/**
 * Message limits response
 */
export interface MessageLimits {
  total_today: number;
  to_official: number | null;
  daily_limit: number;
  official_limit: number | null;
  is_exceeded: boolean;
}

/**
 * Validation response
 */
export interface ValidationResponse {
  allowed: boolean;
  reason: string | null;
  code: string | null;
  current: number | null;
  limit: number | null;
}

/**
 * Message create request
 */
export interface MessageCreateRequest {
  sender_id: number;
  recipient_id: number;
  content: string;
}

/**
 * Contact exchange create request
 */
export interface ContactExchangeCreateRequest {
  from_user_id: number;
  to_user_id: number;
}

/**
 * Contact exchange action request
 */
export interface ContactExchangeActionRequest {
  user_id: number;
}
