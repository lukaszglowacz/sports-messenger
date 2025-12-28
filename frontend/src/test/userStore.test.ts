import { describe, it, expect, beforeEach } from 'vitest';
import { useUserStore } from '../store/userStore';
import type { User, ContactInfo, Message } from '../types';

describe('userStore', () => {
  beforeEach(() => {
    useUserStore.setState({
      currentUserId: null,
      currentUser: null,
      selectedContact: null,
      messages: [],
      refreshTrigger: 0,
    });
  });

  it('should set current user', () => {
    const user: User = {
      id: 1,
      name: 'Test',
      email: 'test@test.com',
      type: 'ATHLETE',
    };

    useUserStore.getState().setCurrentUser(1, user);

    expect(useUserStore.getState().currentUserId).toBe(1);
    expect(useUserStore.getState().currentUser).toEqual(user);
  });

  it('should add message to array', () => {
    const message: Message = {
      id: 1,
      sender_id: 1,
      recipient_id: 2,
      content: 'Test',
      created_at: new Date().toISOString(),
    };

    useUserStore.getState().addMessage(message);

    expect(useUserStore.getState().messages).toHaveLength(1);
  });
});