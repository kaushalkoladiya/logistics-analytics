'use client';

import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchSystemStatus } from '@/store/slices/systemSlice';
import { Loader2 } from 'lucide-react';

interface PreCalculationOverlayProps {
  children: React.ReactNode;
}

export function PreCalculationOverlay({ children }: PreCalculationOverlayProps) {
  const dispatch = useAppDispatch();
  const { isCalculating, errorMessage } = useAppSelector((state) => state.system);

  useEffect(() => {
    const checkStatus = () => {
      dispatch(fetchSystemStatus());
    };

    // Initial check
    checkStatus();

    // Poll every 1 min while calculating
    const interval = setInterval(() => {
      if (isCalculating) {
        checkStatus();
      }
    }, 1000 * 60);

    return () => clearInterval(interval);
  }, [dispatch, isCalculating]);

  return (
    <div className="relative">
      {children}

      {isCalculating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm transition-all">
          <div className="rounded-lg bg-white p-6 shadow-lg">
            <div className="flex flex-col items-center space-y-4">
              <Loader2 className="h-8 w-8 animate-spin text-sky-500" />
              <div className="text-center">
                <h3 className="text-lg font-semibold text-slate-900">
                  System Update in Progress
                </h3>
                <p className="mt-1 text-sm text-slate-500">
                  Please wait while we update the analytics data.
                  This may take a few minutes.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {errorMessage && !isCalculating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="rounded-lg bg-white p-6 shadow-lg">
            <div className="flex flex-col items-center space-y-4">
              <div className="rounded-full bg-red-100 p-3">
                <div className="h-6 w-6 text-red-600 text-center">❌</div>
              </div>
              <div className="text-center">
                <h3 className="text-lg font-semibold text-slate-900">
                  Update Failed
                </h3>
                <p className="mt-1 text-sm text-slate-500">
                  {errorMessage}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}