// src/components/shared/date-range-selector.tsx
'use client';

import { useState, useEffect } from 'react';
import { Calendar, ChevronDown } from 'lucide-react';
import { format, subDays, startOfMonth, endOfMonth, subMonths, startOfYear, endOfYear } from 'date-fns';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Calendar as CalendarComponent } from '@/components/ui/calendar';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface DateRangeSelectorProps {
  onDateRangeChange: (range: { start: string; end: string }) => void;
}

type PresetRange = {
  id: string;
  label: string;
  getValue: () => { from: Date; to: Date };
};

const presetRanges: PresetRange[] = [
  {
    id: 'today',
    label: 'Today',
    getValue: () => {
      const today = new Date();
      return { from: today, to: today };
    },
  },
  {
    id: 'last7Days',
    label: 'Last 7 Days',
    getValue: () => ({
      from: subDays(new Date(), 6),
      to: new Date(),
    }),
  },
  {
    id: 'last30Days',
    label: 'Last 30 Days',
    getValue: () => ({
      from: subDays(new Date(), 29),
      to: new Date(),
    }),
  },
  {
    id: 'lastMonth',
    label: 'Last Month',
    getValue: () => {
      const lastMonth = subMonths(new Date(), 1);
      return {
        from: startOfMonth(lastMonth),
        to: endOfMonth(lastMonth),
      };
    },
  },
  {
    id: 'lastYear',
    label: 'Last Year',
    getValue: () => {
      const lastYear = subMonths(new Date(), 12);
      return {
        from: startOfYear(lastYear),
        to: endOfYear(lastYear),
      };
    },
  }
];

export function DateRangeSelector({ onDateRangeChange }: DateRangeSelectorProps) {
  const [date, setDate] = useState<{
    from: Date | undefined;
    to: Date | undefined;
  }>({
    from: undefined,
    to: undefined,
  });
  const [selectedRange, setSelectedRange] = useState('lastYear');

  useEffect(() => {
    const lastYear = presetRanges.find(r => r.id === 'lastYear')!.getValue();
    setDate({ from: lastYear.from, to: lastYear.to });
    onDateRangeChange({
      start: format(lastYear.from, 'yyyy-MM-dd'),
      end: format(lastYear.to, 'yyyy-MM-dd'),
    });
  }, []);

  const handlePresetChange = (presetId: string) => {
    setSelectedRange(presetId);
    
    if (presetId === 'custom') {
      // If selecting custom, just open the calendar popover
      return;
    }

    const preset = presetRanges.find(r => r.id === presetId);
    if (!preset) return;

    const range = preset.getValue();
    setDate({ from: range.from, to: range.to });
    onDateRangeChange({
      start: format(range.from, 'yyyy-MM-dd'),
      end: format(range.to, 'yyyy-MM-dd'),
    });
  };

  const handleCustomDateSelect = (range: { from: Date; to: Date }) => {
    setDate(range);
    if (range.from && range.to) {
      setSelectedRange('custom');
      onDateRangeChange({
        start: format(range.from, 'yyyy-MM-dd'),
        end: format(range.to, 'yyyy-MM-dd'),
      });
    }
  };

  return (
    <div className="flex items-center gap-4">
      <Select 
        value={selectedRange}
        onValueChange={handlePresetChange}
      >
        <SelectTrigger className="w-[160px]">
          <SelectValue placeholder="Select range" />
        </SelectTrigger>
        <SelectContent>
          {presetRanges.map((preset) => (
            <SelectItem key={preset.id} value={preset.id}>
              {preset.label}
            </SelectItem>
          ))}
          <SelectItem value="custom">Custom Range</SelectItem>
        </SelectContent>
      </Select>

      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={cn(
              "justify-start text-left font-normal",
              !date.from && "text-muted-foreground"
            )}
          >
            <Calendar className="mr-2 h-4 w-4" />
            {date.from ? (
              date.to ? (
                <>
                  {format(date.from, "MMM dd, yyyy")} - {format(date.to, "MMM dd, yyyy")}
                </>
              ) : (
                format(date.from, "MMM dd, yyyy")
              )
            ) : (
              <span>Pick a date</span>
            )}
            <ChevronDown className="ml-auto h-4 w-4 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <CalendarComponent
            initialFocus
            mode="range"
            defaultMonth={date.from}
            selected={date}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            onSelect={handleCustomDateSelect as any}
            numberOfMonths={2}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}