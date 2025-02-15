'use client';

import { useEffect, useState } from 'react';
import { Calendar } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import dayjs from 'dayjs';

interface TrendInterval {
  type: 'week' | 'month' | 'year';
  label: string;
  interval: string;
}

const intervals: TrendInterval[] = [
  { type: 'week', label: 'Weekly', interval: 'week' },
  { type: 'month', label: 'Monthly', interval: 'month' },
  { type: 'year', label: 'Yearly', interval: 'year' }
];

export interface OnIntervalChangeParams {
  start: string;
  end: string;
  interval: string;
  periodsBack: number;
}

interface TrendIntervalSelectorProps {
  onIntervalChange: (params: OnIntervalChangeParams) => void;
}

const periodOptions = Array.from({ length: 12 }, (_, i) => i + 1);

export function TrendIntervalSelector({ onIntervalChange }: TrendIntervalSelectorProps) {
  const [selectedInterval, setSelectedInterval] = useState<TrendInterval>(intervals[0]);
  const [periodsBack, setPeriodsBack] = useState<number>(1);
  const [dateRange, setDateRange] = useState<{ start: string; end: string }>({
    start: dayjs().subtract(1, 'week').startOf('week').format('YYYY-MM-DD'),
    end: dayjs().subtract(1, 'week').endOf('week').format('YYYY-MM-DD')
  });

  useEffect(() => {
    onIntervalChange({
      start: dateRange.start,
      end: dateRange.end,
      interval: selectedInterval.interval,
      periodsBack
    });
  }, []);

  const calculateStartDate = (interval: string, periods: number) => {
    const currentDate = dayjs();
    let startDate = currentDate.startOf('day');

    switch (interval) {
      case 'week':
        startDate = currentDate.startOf('week').subtract(periods, 'week');
        break;
      case 'month':
        startDate = currentDate.startOf('month').subtract(periods, 'month');
        break;
      case 'year':
        startDate = currentDate.startOf('year').subtract(periods, 'year');
        break;
      default:
        break;
    }
    return startDate.format('YYYY-MM-DD');
  };

  const calculateEndDate = (interval: string, periods: number) => {
    const currentDate = dayjs();
    let endDate = currentDate.endOf('day');

    switch (interval) {
      case 'week':
        endDate = currentDate.endOf('week').subtract(periods, 'week').endOf('week');
        break;
      case 'month':
        endDate = currentDate.endOf('month').subtract(periods, 'month').endOf('month');
        break;
      case 'year':
        endDate = currentDate.endOf('year').subtract(periods, 'year').endOf('year');
        break;
      default:
        break;
    }
    return endDate.format('YYYY-MM-DD');
  };

  const handleIntervalChange = (type: 'week' | 'month' | 'year') => {
    const interval = intervals.find(i => i.type === type);
    if (interval) {
      setSelectedInterval(interval);
      const start = calculateStartDate(interval.interval, periodsBack);
      const end = calculateEndDate(interval.interval, periodsBack);
      setDateRange({ start, end });
      onIntervalChange({
        start,
        end,
        interval: `${periodsBack} ${interval.interval}`,
        periodsBack
      });
    }
  };

  const handlePeriodsChange = (value: string) => {
    const periods = parseInt(value) || 1;
    setPeriodsBack(periods);
    const start = calculateStartDate(selectedInterval.interval, periods);
    const end = calculateEndDate(selectedInterval.interval, periods);
    setDateRange({ start, end });
    onIntervalChange({
      start,
      end,
      interval: `${periods} ${selectedInterval.interval}`,
      periodsBack: periods
    });
  };

  return (
    <div className="flex flex-col items-start gap-6">
      <div className="flex items-center gap-2">
        <Select
          value={selectedInterval.type}
          onValueChange={handleIntervalChange}
        >
          <SelectTrigger className="w-[180px]">
            <Calendar className="mr-2 h-4 w-4" />
            <SelectValue placeholder="Select interval" />
          </SelectTrigger>
          <SelectContent>
            {intervals.map((interval) => (
              <SelectItem key={interval.type} value={interval.type}>
                {interval.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          value={periodsBack.toString()}
          onValueChange={handlePeriodsChange}
        >
          <SelectTrigger className="w-[120px]">
            <SelectValue placeholder="Select periods" />
          </SelectTrigger>
          <SelectContent>
            {periodOptions.map((num) => (
              <SelectItem key={num} value={num.toString()}>
                {num} {num === 1 ? selectedInterval.interval : `${selectedInterval.interval}s`}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <span className="text-sm text-slate-500">Past X months/weeks/years</span>
      </div>

      <div className="mt-4 text-sm text-slate-600">
        <p>
          <span className="font-semibold">Selected Range:</span> {dateRange.start} - {dateRange.end}
        </p>
      </div>
    </div>
  );
}