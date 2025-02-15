import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '@/lib/axios';
import { ENDPOINTS } from '@/constants/endpoints';

interface SystemState {
  isCalculating: boolean;
  lastCalculatedAt: string | null;
  errorMessage: string | null;
}

const initialState: SystemState = {
  isCalculating: false,
  lastCalculatedAt: null,
  errorMessage: null,
};

export const fetchSystemStatus = createAsyncThunk(
  'system/fetchStatus',
  async () => {
    const response = await api.get(ENDPOINTS.SYSTEM.STATUS);
    return response.data;
  }
);

const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchSystemStatus.fulfilled, (state, action) => {
        state.isCalculating = action.payload.is_calculating;
        state.lastCalculatedAt = action.payload.last_calculated_at;
        state.errorMessage = action.payload.error_message;
      });
  },
});

export default systemSlice.reducer;