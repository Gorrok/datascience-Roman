import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://datascience-roman-production.up.railway.app/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
});

export const api = {
  async getPlans(userId, { includeCompleted = false, onlyCompleted = false } = {}) {
    const response = await client.get('/plans/', {
      params: {
        user_id: userId,
        include_completed: includeCompleted,
        only_completed: onlyCompleted,
      }
    });
    return response.data;
  },

  async getStats(userId) {
    const response = await client.get(`/plans/stats/${userId}`);
    return response.data;
  },

  async createPlan(planData) {
    const response = await client.post('/plans/', planData);
    return response.data;
  },

  async updatePlan(planId, planData) {
    const response = await client.patch(`/plans/${planId}`, planData);
    return response.data;
  },

  async deletePlan(planId) {
    const response = await client.delete(`/plans/${planId}`);
    return response.data;
  },

  async createInvite(inviteData) {
    const response = await client.post('/plans/invites', inviteData);
    return response.data;
  },

  async getInvites(userId, status = null) {
    const response = await client.get(`/plans/invites/${userId}`, {
      params: status ? { status } : {}
    });
    return response.data;
  },

  async respondToInvite(inviteId, status) {
    const response = await client.patch(`/plans/invites/${inviteId}/respond`, null, {
      params: { status },
    });
    return response.data;
  },
};
