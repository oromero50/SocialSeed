/**
 * Dashboard Component Tests
 * Comprehensive testing for the main SocialSeed dashboard
 */

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Dashboard from '../components/Dashboard'

// Mock data
const mockAccounts = [
  {
    id: '1',
    platform: 'tiktok',
    username: 'test_tiktok',
    is_active: true,
    health_score: 0.95,
    current_phase: 'phase_1',
    daily_action_limit: 50,
    created_at: '2024-01-01T00:00:00Z'
  },
  {
    id: '2',
    platform: 'instagram',
    username: 'test_instagram',
    is_active: true,
    health_score: 0.87,
    current_phase: 'phase_2',
    daily_action_limit: 75,
    created_at: '2024-01-15T00:00:00Z'
  }
]

const mockPendingApprovals = [
  {
    id: '1',
    account_id: '1',
    action_type: 'follow',
    target_account: 'target_user',
    risk_level: 'yellow',
    created_at: '2024-01-01T12:00:00Z'
  }
]

// Mock Supabase responses
const mockSupabase = {
  from: jest.fn(() => ({
    select: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    update: jest.fn().mockReturnThis(),
    delete: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    order: jest.fn().mockReturnThis(),
    limit: jest.fn().mockReturnThis(),
    single: jest.fn(),
  })),
}

jest.mock('../lib/supabase', () => ({
  supabase: mockSupabase,
}))

describe('Dashboard Component', () => {
  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks()
    
    // Setup default mock responses
    mockSupabase.from.mockImplementation((table) => {
      const mockChain = {
        select: jest.fn().mockReturnThis(),
        insert: jest.fn().mockReturnThis(),
        update: jest.fn().mockReturnThis(),
        delete: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        order: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        single: jest.fn(),
      }

      if (table === 'social_accounts') {
        mockChain.select.mockResolvedValue({ data: mockAccounts, error: null })
      } else if (table === 'actions') {
        mockChain.select.mockResolvedValue({ data: mockPendingApprovals, error: null })
      }

      return mockChain
    })
  })

  describe('Rendering', () => {
    it('renders dashboard title and main sections', async () => {
      render(<Dashboard />)
      
      expect(screen.getByText('SocialSeed Dashboard')).toBeInTheDocument()
      expect(screen.getByText('Account Overview')).toBeInTheDocument()
      expect(screen.getByText('Pending Approvals')).toBeInTheDocument()
    })

    it('displays loading state initially', () => {
      render(<Dashboard />)
      
      expect(screen.getByText('Loading...')).toBeInTheDocument()
    })

    it('renders accounts after loading', async () => {
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('test_tiktok')).toBeInTheDocument()
        expect(screen.getByText('test_instagram')).toBeInTheDocument()
      })
    })
  })

  describe('Account Management', () => {
    it('opens add account modal when button is clicked', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('test_tiktok')).toBeInTheDocument()
      })
      
      const addButton = screen.getByText('Add Account')
      await user.click(addButton)
      
      expect(screen.getByText('Add Social Media Account')).toBeInTheDocument()
    })

    it('validates add account form', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Add Account')).toBeInTheDocument()
      })
      
      const addButton = screen.getByText('Add Account')
      await user.click(addButton)
      
      // Try to submit without filling form
      const submitButton = screen.getByText('Add Account')
      await user.click(submitButton)
      
      // Should show validation errors
      expect(screen.getByText('Username is required')).toBeInTheDocument()
    })

    it('submits add account form with valid data', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Add Account')).toBeInTheDocument()
      })
      
      const addButton = screen.getByText('Add Account')
      await user.click(addButton)
      
      // Fill form
      const usernameInput = screen.getByLabelText('Username')
      await user.type(usernameInput, 'new_test_account')
      
      const platformSelect = screen.getByLabelText('Platform')
      await user.selectOptions(platformSelect, 'tiktok')
      
      // Submit form
      const submitButton = screen.getByText('Add Account')
      await user.click(submitButton)
      
      // Should call Supabase insert
      expect(mockSupabase.from).toHaveBeenCalledWith('social_accounts')
    })
  })

  describe('Account Actions', () => {
    it('displays account health scores', async () => {
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('95%')).toBeInTheDocument() // TikTok health
        expect(screen.getByText('87%')).toBeInTheDocument() // Instagram health
      })
    })

    it('shows correct phase for each account', async () => {
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Phase 1')).toBeInTheDocument()
        expect(screen.getByText('Phase 2')).toBeInTheDocument()
      })
    })

    it('allows editing account settings', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('test_tiktok')).toBeInTheDocument()
      })
      
      // Click edit button for first account
      const editButtons = screen.getAllByText('Edit')
      await user.click(editButtons[0])
      
      expect(screen.getByText('Edit Account')).toBeInTheDocument()
    })
  })

  describe('Approval Workflow', () => {
    it('displays pending approvals', async () => {
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('target_user')).toBeInTheDocument()
        expect(screen.getByText('follow')).toBeInTheDocument()
      })
    })

    it('allows approving actions', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Approve')).toBeInTheDocument()
      })
      
      const approveButton = screen.getByText('Approve')
      await user.click(approveButton)
      
      // Should make API call to approve
      expect(mockSupabase.from).toHaveBeenCalledWith('actions')
    })

    it('allows rejecting actions', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Reject')).toBeInTheDocument()
      })
      
      const rejectButton = screen.getByText('Reject')
      await user.click(rejectButton)
      
      // Should make API call to reject
      expect(mockSupabase.from).toHaveBeenCalledWith('actions')
    })
  })

  describe('Real-time Updates', () => {
    it('refreshes data periodically', async () => {
      jest.useFakeTimers()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('test_tiktok')).toBeInTheDocument()
      })
      
      // Fast-forward time to trigger refresh
      jest.advanceTimersByTime(30000) // 30 seconds
      
      // Should make additional API calls
      expect(mockSupabase.from).toHaveBeenCalledTimes(4) // Initial load + refresh
      
      jest.useRealTimers()
    })
  })

  describe('Error Handling', () => {
    it('displays error message when data loading fails', async () => {
      // Mock error response
      mockSupabase.from.mockImplementation(() => ({
        select: jest.fn().mockReturnThis(),
        order: jest.fn().mockReturnThis(),
        eq: jest.fn().mockResolvedValue({ data: null, error: { message: 'Network error' } }),
      }))
      
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Error loading data')).toBeInTheDocument()
      })
    })

    it('handles network errors gracefully', async () => {
      // Mock network failure
      mockSupabase.from.mockImplementation(() => ({
        select: jest.fn().mockReturnThis(),
        order: jest.fn().mockReturnThis(),
        eq: jest.fn().mockRejectedValue(new Error('Network error')),
      }))
      
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('Network error occurred')).toBeInTheDocument()
      })
    })
  })

  describe('Responsive Design', () => {
    it('adapts layout for mobile screens', () => {
      // Mock mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      })
      
      render(<Dashboard />)
      
      // Should apply mobile-specific styles
      expect(screen.getByTestId('dashboard-container')).toHaveClass('mobile-layout')
    })
  })

  describe('Performance', () => {
    it('memoizes expensive calculations', async () => {
      const renderSpy = jest.spyOn(React, 'useMemo')
      
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('test_tiktok')).toBeInTheDocument()
      })
      
      expect(renderSpy).toHaveBeenCalled()
      renderSpy.mockRestore()
    })

    it('debounces search input', async () => {
      const user = userEvent.setup()
      render(<Dashboard />)
      
      await waitFor(() => {
        expect(screen.getByText('test_tiktok')).toBeInTheDocument()
      })
      
      const searchInput = screen.getByPlaceholderText('Search accounts...')
      
      // Type rapidly
      await user.type(searchInput, 'test')
      
      // Should debounce API calls
      expect(mockSupabase.from).toHaveBeenCalledTimes(2) // Only initial load, not search calls yet
    })
  })
})

