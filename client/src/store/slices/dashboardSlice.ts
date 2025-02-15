import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '@/lib/axios';
import { ENDPOINTS } from '@/constants/endpoints';
import { OnIntervalChangeParams } from '@/components/trends/trend-interval-selector';
import { AnalyticsState, DashboardOverview } from '@/types/dashboard';

const initialState: AnalyticsState = {
  data: null,
  loading: false,
  error: null
};

export const fetchDashboard = createAsyncThunk(
  'dashboard/fetchDashboard',
  async (params: OnIntervalChangeParams) => {
    const response = await apiService.get<DashboardOverview>(
      ENDPOINTS.DASHBOARD,
      {
        start: params.start,
        end: params.end,
        interval_type: params.interval,
        periods_back: params.periodsBack,
      }
    );
    return response;
  }
);

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    clearDashboard: (state) => {
      state.data = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboard.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDashboard.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchDashboard.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch daily totals';
      })
  },
});

export const { clearDashboard } = dashboardSlice.actions;
export default dashboardSlice.reducer;