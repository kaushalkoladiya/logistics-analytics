import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '@/lib/axios';
import { ENDPOINTS } from '@/constants/endpoints';
import type {
  VehicleState,
  VehicleMetric,
  VehicleDetail,
  VehicleDetailsRequest
} from '@/types/vehicles';

const initialState: VehicleState = {
  metrics: {
    data: null,
    loading: false,
    error: null,
  },
  detail: {
    data: null,
    loading: false,
    error: null,
  }
};

export const fetchVehicleMetrics = createAsyncThunk(
  'vehicles/fetchMetrics',
  async ({ start, end }: { start: string; end: string }) => {
    const response = await api.get<VehicleMetric[]>(ENDPOINTS.VEHICLES.METRICS, {
      params: { start, end }
    });
    return response.data;
  }
);

export const fetchVehicleDetails = createAsyncThunk(
  'vehicles/fetchDetails',
  async ({ end, id, start }: VehicleDetailsRequest) => {
    const response = await api.get<VehicleDetail>(
      `${ENDPOINTS.VEHICLES.DETAILS}/${id}/details`,
      {
        params: { start, end }
      }
    );
    return response.data;
  },
  {
    condition: (_, { getState }) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const { vehicles } = getState() as any;
      return !vehicles.detail.loading; // Avoid dispatching if already loading
    }
  }
);

const vehicleSlice = createSlice({
  name: 'vehicles',
  initialState,
  reducers: {
    clearVehicleDetails: (state) => {
      state.detail.data = null;
      state.detail.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchVehicleMetrics.pending, (state) => {
        state.metrics.loading = true;
        state.metrics.error = null;
      })
      .addCase(fetchVehicleMetrics.fulfilled, (state, action) => {
        state.metrics.loading = false;
        state.metrics.data = action.payload;
      })
      .addCase(fetchVehicleMetrics.rejected, (state, action) => {
        state.metrics.loading = false;
        state.metrics.error = action.error.message || 'Failed to fetch vehicle metrics';
      })
      .addCase(fetchVehicleDetails.pending, (state) => {
        state.detail.loading = true;
        state.detail.error = null;
      })
      .addCase(fetchVehicleDetails.fulfilled, (state, action) => {
        state.detail.loading = false;
        state.detail.data = action.payload;
      })
      .addCase(fetchVehicleDetails.rejected, (state, action) => {
        state.detail.loading = false;
        state.detail.error = action.error.message || 'Failed to fetch vehicle details';
      });
  },
});

export default vehicleSlice.reducer;
export const { clearVehicleDetails } = vehicleSlice.actions;