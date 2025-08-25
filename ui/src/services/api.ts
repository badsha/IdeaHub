import axios from 'axios'
import toast from 'react-hot-toast'

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth header if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Add debug auth header for testing
    // Vite uses import.meta.env instead of process.env
    if (import.meta.env.MODE === 'development') {
      config.headers['X-Debug-Auth'] = 'authenticated'
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const message = error.response?.data?.message || error.message || 'An error occurred'
    
    // Show error toast
    toast.error(message)
    
    return Promise.reject(error)
  }
)

// API endpoints
export const endpoints = {
  // Health checks
  health: '/health',
  healthDetailed: '/health/detailed',
  healthReady: '/health/ready',
  
  // Workspaces
  workspaces: '/workspaces',
  workspace: (id: number) => `/workspaces/${id}`,
  
  // Communities
  communities: '/communities',
  community: (id: number) => `/communities/${id}`,
  
  // Ideas
  ideas: '/ideas',
  idea: (id: number) => `/ideas/${id}`,
  
  // Search
  search: '/search',
}

// API functions
export const apiService = {
  // Health checks
  async getHealth() {
    const response = await api.get(endpoints.health)
    return response.data
  },
  
  async getDetailedHealth() {
    const response = await api.get(endpoints.healthDetailed)
    return response.data
  },
  
  // Workspaces
  async getWorkspaces() {
    const response = await api.get(endpoints.workspaces)
    return response.data
  },
  
  async getWorkspace(id: number) {
    const response = await api.get(endpoints.workspace(id))
    return response.data
  },
  
  async createWorkspace(data: any) {
    const response = await api.post(endpoints.workspaces, data)
    return response.data
  },
  
  async updateWorkspace(id: number, data: any) {
    const response = await api.put(endpoints.workspace(id), data)
    return response.data
  },
  
  async deleteWorkspace(id: number) {
    const response = await api.delete(endpoints.workspace(id))
    return response.data
  },
  
  // Communities
  async getCommunities() {
    const response = await api.get(endpoints.communities)
    return response.data
  },
  
  async getCommunity(id: number) {
    const response = await api.get(endpoints.community(id))
    return response.data
  },
  
  async createCommunity(data: any) {
    const response = await api.post(endpoints.communities, data)
    return response.data
  },
  
  async updateCommunity(id: number, data: any) {
    const response = await api.put(endpoints.community(id), data)
    return response.data
  },
  
  async deleteCommunity(id: number) {
    const response = await api.delete(endpoints.community(id))
    return response.data
  },
  
  // Ideas
  async getIdeas() {
    const response = await api.get(endpoints.ideas)
    return response.data
  },
  
  async getIdea(id: number) {
    const response = await api.get(endpoints.idea(id))
    return response.data
  },
  
  async createIdea(data: any) {
    const response = await api.post(endpoints.ideas, data)
    return response.data
  },
  
  async updateIdea(id: number, data: any) {
    const response = await api.put(endpoints.idea(id), data)
    return response.data
  },
  
  async deleteIdea(id: number) {
    const response = await api.delete(endpoints.idea(id))
    return response.data
  },
  
  // Search
  async search(query: string) {
    const response = await api.get(endpoints.search, {
      params: { q: query }
    })
    return response.data
  },
}

export default api
