import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '@/lib/axios';
import type { ShipmentState, ShipmentAnalytics, RouteParams, PaginatedRouteResponse } from '@/types/shipments';
import { ENDPOINTS } from '@/constants/endpoints';

const initialState: ShipmentState = {
  analytics: {
    data: null,
    loading: false,
    error: null,
  },
  routes: {
    data: [],
    total: 0,
    page: 1,
    pageSize: 10,
    loading: false,
    error: null,
  },
};

export const fetchShipmentAnalytics = createAsyncThunk(
  'shipments/fetchAnalytics',
  async ({ start, end }: { start: string; end: string }) => {
    const response = await api.get<ShipmentAnalytics>(ENDPOINTS.SHIPMENTS.ANALYTICS, {
      params: { start, end }
    });
    return response.data;
  }
);

export const fetchRoutePerformance = createAsyncThunk(
  'shipments/fetchRoutes',
  async (params: RouteParams) => {
    const response = await api.get<PaginatedRouteResponse>(ENDPOINTS.SHIPMENTS.ROUTES, {
      params: {
        page: params.page,
        page_size: params.pageSize,
        sort_by: params.sortBy,
        sort_order: params.sortOrder,
        search: params.search
      }
    });
    return response.data;
  }
);

const shipmentSlice = createSlice({
  name: 'shipments',
  initialState,
  reducers: {
    clearShipmentAnalytics: (state) => {
      state.analytics.data = null;
      state.analytics.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchShipmentAnalytics.pending, (state) => {
        state.analytics.loading = true;
        state.analytics.error = null;
      })
      .addCase(fetchShipmentAnalytics.fulfilled, (state, action) => {
        state.analytics.loading = false;
        state.analytics.data = action.payload;
      })
      .addCase(fetchShipmentAnalytics.rejected, (state, action) => {
        state.analytics.loading = false;
        state.analytics.error = action.error.message || 'Failed to fetch shipment analytics';
      })
      .addCase(fetchRoutePerformance.pending, (state) => {
        state.routes.loading = true;
        state.routes.error = null;
      })
      .addCase(fetchRoutePerformance.fulfilled, (state, action) => {
        state.routes.loading = false;
        state.routes.data = action.payload.data;
        state.routes.total = action.payload.total;
        state.routes.page = action.payload.page;
        state.routes.pageSize = action.payload.page_size;
      })
      .addCase(fetchRoutePerformance.rejected, (state, action) => {
        state.routes.loading = false;
        state.routes.error = action.error.message || 'Failed to fetch routes';
      });
  },
});

export const { clearShipmentAnalytics } = shipmentSlice.actions;
export default shipmentSlice.reducer;