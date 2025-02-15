import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '@/lib/axios';
import type {
  RouteState,
  TopRoutePerformance,
  RouteAPIRequest,
  RouteReliabilityResponse,
  RouteCostValueResponse,
  RouteOptimizationResponse
} from '@/types/routes';
import { ENDPOINTS } from '@/constants/endpoints';

const initialState: RouteState = {
  reliability: {
    data: [],
    loading: false,
    error: null,
    page: 1,
    pageSize: 10,
    total: 0,
  },
  costValue: {
    data: [],
    loading: false,
    error: null,
    page: 1,
    pageSize: 10,
    total: 0,
  },
  optimization: {
    data: [],
    loading: false,
    error: null,
    page: 1,
    pageSize: 10,
    total: 0,
  },
  topPerforming: {
    data: [],
    loading: false,
    error: null,
    page: 1,
    pageSize: 10,
    total: 0,
  },
};

export const fetchRouteReliability = createAsyncThunk(
  'route/fetchReliability',
  async ({ start, end, page, pageSize, search, sortBy, sortOrder }: RouteAPIRequest) => {
    const response = await api.get<RouteReliabilityResponse>(
      ENDPOINTS.ROUTES.RELIABILITY,
      {
        params: {
          start,
          end,
          page,
          page_size: pageSize,
          search,
          sort_by: sortBy,
          sort_order: sortOrder
        }
      }
    );

    return response.data;
  }
);

export const fetchRouteCostValue = createAsyncThunk(
  'route/fetchCostValue',
  async ({ start, end, page, pageSize, search, sortBy, sortOrder }: RouteAPIRequest) => {
    const response = await api.get<RouteCostValueResponse>(
      ENDPOINTS.ROUTES.COST_VALUE,
      {
        params: {
          start,
          end,
          page,
          page_size: pageSize,
          search,
          sort_by: sortBy,
          sort_order: sortOrder
        }
      }
    );
    return response.data;
  }
);

export const fetchRouteOptimization = createAsyncThunk(
  'route/fetchOptimization',
  async ({ start, end, page, pageSize, search, sortBy, sortOrder }: RouteAPIRequest) => {
    const response = await api.get<RouteOptimizationResponse>(
      ENDPOINTS.ROUTES.OPTIMIZATION,
      {
        params: {
          start,
          end,
          page,
          page_size: pageSize,
          search,
          sort_by: sortBy,
          sort_order: sortOrder
        }
      }
    );
    return response.data;
  }
);

export const fetchTopPerformingRoutes = createAsyncThunk(
  'route/fetchTopPerforming',
  async ({ start, end, limit = 10 }: { start: string; end: string; limit?: number }) => {
    const response = await api.get<TopRoutePerformance[]>(
      ENDPOINTS.ROUTES.TOP_ROUTES,
      { params: { start, end, limit } }
    );
    return response.data;
  }
);

const routeSlice = createSlice({
  name: 'route',
  initialState,
  reducers: {
    clearRoute: (state) => {
      state.reliability.data = [];
      state.costValue.data = [];
      state.optimization.data = [];
      state.reliability.error = null;
      state.costValue.error = null;
      state.optimization.error = null;
    },
  },
  extraReducers: (builder) => {
    // Reliability
    builder
      // .addCase(fetchRouteReliability.pending, (state) => {
      //   state.reliability.loading = true;
      //   state.reliability.error = null;
      // })
      .addCase(fetchRouteReliability.fulfilled, (state, action) => {
        state.reliability.loading = false;
        state.reliability.data = action.payload.data;
        state.reliability.page = action.payload.page;
        state.reliability.pageSize = action.payload.pageSize;
        state.reliability.total = action.payload.total;
      })
      .addCase(fetchRouteReliability.rejected, (state, action) => {
        state.reliability.loading = false;
        state.reliability.error = action.error.message || 'Failed to fetch route reliability';
      })
      // Cost Value
      // .addCase(fetchRouteCostValue.pending, (state) => {
      //   state.costValue.loading = true;
      //   state.costValue.error = null;
      // })
      .addCase(fetchRouteCostValue.fulfilled, (state, action) => {
        state.costValue.loading = false;
        state.costValue.data = action.payload.data;
        state.costValue.page = action.payload.page;
        state.costValue.pageSize = action.payload.pageSize;
        state.costValue.total = action.payload.total;
      })
      .addCase(fetchRouteCostValue.rejected, (state, action) => {
        state.costValue.loading = false;
        state.costValue.error = action.error.message || 'Failed to fetch route cost value';
      })
      // Optimization
      // .addCase(fetchRouteOptimization.pending, (state) => {
      //   state.optimization.loading = true;
      //   state.optimization.error = null;
      // })
      .addCase(fetchRouteOptimization.fulfilled, (state, action) => {
        state.optimization.loading = false;
        state.optimization.data = action.payload.data;
        state.optimization.page = action.payload.page;
        state.optimization.pageSize = action.payload.pageSize;
        state.optimization.total = action.payload.total;
      })
      .addCase(fetchRouteOptimization.rejected, (state, action) => {
        state.optimization.loading = false;
        state.optimization.error = action.error.message || 'Failed to fetch route optimization';
      })
      // Top Performing
      // .addCase(fetchTopPerformingRoutes.pending, (state) => {
      //   state.topPerforming.loading = true;
      //   state.topPerforming.error = null;
      // })
      .addCase(fetchTopPerformingRoutes.fulfilled, (state, action) => {
        state.topPerforming.loading = false;
        state.topPerforming.data = action.payload;
      })
      .addCase(fetchTopPerformingRoutes.rejected, (state, action) => {
        state.topPerforming.loading = false;
        state.topPerforming.error = action.error.message || 'Failed to fetch top performing routes';
      });
  },
});

export const { clearRoute } = routeSlice.actions;
export default routeSlice.reducer;