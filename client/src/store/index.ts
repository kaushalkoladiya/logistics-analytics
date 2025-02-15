import { configureStore } from '@reduxjs/toolkit';
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';

import dashboardReducer from './slices/dashboardSlice';
import vehiclesReducer from './slices/vehicleSlice';
import shipmentsReducer from './slices/shipmentSlice';
import routeReducer from './slices/routeSlice';
import costsReducer from './slices/costSlice';
import systemReducer from './slices/systemSlice';

export const store = configureStore({
  reducer: {
    dashboard: dashboardReducer,
    vehicles: vehiclesReducer,
    shipments: shipmentsReducer,
    route: routeReducer,
    costs: costsReducer,
    system: systemReducer,
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;