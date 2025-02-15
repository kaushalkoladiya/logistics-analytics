import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '@/lib/axios';
import type { CostOverview, CostState } from '@/types/costs';
import { ENDPOINTS } from '@/constants/endpoints';

const initialState: CostState = {
  overview: {
    data: null,
    loading: true,
    error: null,
  }
};

export const fetchCostOverview = createAsyncThunk(
  'costs/fetchOverview',
  async ({ start, end }: { start: string; end: string }) => {
    const response = await api.get<CostOverview>(ENDPOINTS.COSTS.OVERVIEW, {
      params: { start, end }
    });
    return response.data;
  }
);

const costSlice = createSlice({
  name: 'costs',
  initialState,
  reducers: {
    clearCostOverview: (state) => {
      state.overview.data = null;
      state.overview.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCostOverview.fulfilled, (state, action) => {
        state.overview.loading = false;
        state.overview.data = action.payload;
      })
      .addCase(fetchCostOverview.rejected, (state, action) => {
        state.overview.loading = false;
        state.overview.error = action.error.message || 'Failed to fetch cost overview';
      })
  },
});

export const { clearCostOverview } = costSlice.actions;
export default costSlice.reducer;