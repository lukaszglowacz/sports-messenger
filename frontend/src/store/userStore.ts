/**
 * Zustand store for managing application state.
 * 
 * Manages:
 * - Current user ID (for user switcher)
 * - Selected contact
 * - Contact list
 * - Messages
 */

import { create } from 'zustand';
import type { User, ContactInfo, Message, ContactListResponse } from '../types';

interface UserStore {
  // Current user (selected from switcher)
  currentUserId: number | null;
  currentUser: User | null;
  setCurrentUser: (userId: number, user: User) => void;

  // Selected contact for chat
  selectedContact: ContactInfo | null;
  setSelectedContact: (contact: ContactInfo | null) => void;

  // Contact list
  contactList: ContactListResponse | null;
  setContactList: (contacts: ContactListResponse) => void;

  // Messages for current conversation
  messages: Message[];
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;

  // Refresh trigger
  refreshTrigger: number;
  triggerRefresh: () => void;
}

/**
 * Global state store using Zustand.
 * 
 * Usage:
 *   const currentUserId = useUserStore(state => state.currentUserId);
 *   const setCurrentUser = useUserStore(state => state.setCurrentUser);
 */
export const useUserStore = create<UserStore>((set) => ({
  // Initial state
  currentUserId: 1, // Default to Zawodnik 1
  currentUser: null,
  selectedContact: null,
  contactList: null,
  messages: [],
  refreshTrigger: 0,

  // Actions
  setCurrentUser: (userId, user) =>
    set({
      currentUserId: userId,
      currentUser: user,
      selectedContact: null, // Clear selected contact when switching users
      messages: [], // Clear messages
    }),

  setSelectedContact: (contact) =>
    set({
      selectedContact: contact,
      messages: [], // Clear messages when switching contacts
    }),

  setContactList: (contacts) =>
    set({ contactList: contacts }),

  setMessages: (messages) =>
    set({ messages }),

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  triggerRefresh: () =>
    set((state) => ({
      refreshTrigger: state.refreshTrigger + 1,
    })),
}));
