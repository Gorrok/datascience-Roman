import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = {
  // Plans
  async getPlans(userId, includeCompleted = false) {
    const response = await axios.get(`${API_BASE_URL}/plans/`, {
      params: { user_id: userId, include_completed: includeCompleted }
    });
    return response.data;
  },

  async createPlan(planData) {
    const response = await axios.post(`${API_BASE_URL}/plans/`, planData);
    return response.data;
  },

  async updatePlan(planId, planData) {
    const response = await axios.patch(`${API_BASE_URL}/plans/${planId}`, planData);
    return response.data;
  },

  async deletePlan(planId) {
    const response = await axios.delete(`${API_BASE_URL}/plans/${planId}`);
    return response.data;
  },

  // Invites
  async createInvite(inviteData) {
    const response = await axios.post(`${API_BASE_URL}/plans/invites`, inviteData);
    return response.data;
  },

  async getInvites(userId, status = null) {
    const response = await axios.get(`${API_BASE_URL}/plans/invites/${userId}`, {
      params: status ? { status } : {}
    });
    return response.data;
  }
};
