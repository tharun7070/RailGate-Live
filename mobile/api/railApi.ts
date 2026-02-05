import axios from 'axios';

// Change this to your backend URL
// For local development on physical device, use your computer's IP address
// For emulator, use 10.0.2.2 (Android) or localhost (iOS)
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface Crossing {
    id: string;
    name: string;
    location: string;
    latitude: number;
    longitude: number;
    nearest_station_code: string;
    nearest_station_name: string;
    distance_to_station_km: number;
    avg_close_duration_mins: number;
    buffer_minutes: number;
    reliability_score: number;
    current_status: string;
    last_updated: string;
    is_active: boolean;
    detour_distance_km?: number;
    detour_time_mins?: number;
}

export interface CrossingStatus extends Crossing {
    prediction: {
        status: string;
        confidence: number;
        next_closure: string | null;
        estimated_duration_mins: number | null;
        time_until_closure_mins: number | null;
        trains_approaching: number;
        closure_windows: any[];
        crowd_confirmations: number;
        last_crowd_update: string | null;
        detour_recommendation: any;
    };
}

export interface Feedback {
    crossing_id: string;
    actual_status: 'open' | 'closed';
    notes?: string;
}

// API Functions
export const railApi = {
    // Get all crossings
    getCrossings: async (): Promise<Crossing[]> => {
        const response = await api.get('/crossings/');
        return response.data;
    },

    // Get specific crossing
    getCrossing: async (crossingId: string): Promise<Crossing> => {
        const response = await api.get(`/crossings/${crossingId}`);
        return response.data;
    },

    // Get crossing status with prediction
    getCrossingStatus: async (crossingId: string): Promise<CrossingStatus> => {
        const response = await api.get(`/crossings/${crossingId}/status`);
        return response.data;
    },

    // Submit feedback
    submitFeedback: async (feedback: Feedback): Promise<any> => {
        const response = await api.post('/feedback/', feedback);
        return response.data;
    },

    // Get recent feedback
    getRecentFeedback: async (crossingId: string, hours: number = 1): Promise<any[]> => {
        const response = await api.get(`/feedback/${crossingId}/recent?hours=${hours}`);
        return response.data;
    },

    // Health check
    healthCheck: async (): Promise<any> => {
        const response = await api.get('/health');
        return response.data;
    },
};

export default railApi;
