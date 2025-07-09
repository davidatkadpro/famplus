import { useState, useEffect } from 'react';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';

export interface ScheduleValue {
  cron: string; // 5-field cron string (min hr dom mon dow)
  startDate: string; // YYYY-MM-DD
  endMode: 'never' | 'on' | 'after';
  endDate?: string;
  endOccurrences?: number;
}

interface SchedulerProps {
  value: ScheduleValue;
  onChange: (v: ScheduleValue) => void;
  className?: string;
}

const weekdays = [
  { label: 'Sun', value: 0 },
  { label: 'Mon', value: 1 },
  { label: 'Tue', value: 2 },
  { label: 'Wed', value: 3 },
  { label: 'Thu', value: 4 },
  { label: 'Fri', value: 5 },
  { label: 'Sat', value: 6 },
];

export function Scheduler({ value, onChange, className }: SchedulerProps) {
  const [freq, setFreq] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>('daily');
  const [time, setTime] = useState('08:00');
  const [interval, setInterval] = useState(1);
  const [weeklyDays, setWeeklyDays] = useState<number[]>([1]);
  const [monthlyDay, setMonthlyDay] = useState(1);
  const [monthlyMode, setMonthlyMode] = useState<'day' | 'nth'>('day');
  const [nthWeek, setNthWeek] = useState<'1' | '2' | '3' | '4' | 'L'>('1');
  const [nthWeekday, setNthWeekday] = useState<number>(1);
  const [yearMonth, setYearMonth] = useState<string>('01-01'); // MM-DD
  const [startDate, setStartDate] = useState(value.startDate);
  const [endMode, setEndMode] = useState<'never' | 'on' | 'after'>(value.endMode);
  const [endDate, setEndDate] = useState(value.endDate || '');
  const [endAfter, setEndAfter] = useState<number>(value.endOccurrences || 0);

  // compute cron whenever inputs change
  const computeCron = () => {
    const [hh, mm] = time.split(':');
    switch (freq) {
      case 'daily':
        return `${mm} ${hh} */${interval} * *`;
      case 'weekly':
        return `${mm} ${hh} * * ${weeklyDays.sort().join(',') || '*'}`;
      case 'monthly':
        if (monthlyMode === 'day') {
          return `${mm} ${hh} ${monthlyDay} */${interval} *`;
        }
        // nth weekday placeholder using cron with '#' supports only some engines, backend can parse
        return `${mm} ${hh} ? */${interval} ${nthWeekday}#${nthWeek === 'L' ? 5 : nthWeek}`;
      case 'yearly':
        const [month, day] = yearMonth.split('-');
        return `${mm} ${hh} ${parseInt(day, 10)} ${parseInt(month, 10)} *`;
    }
  };

  const update = () => {
    onChange({
      cron: computeCron(),
      startDate,
      endMode,
      endDate: endMode === 'on' ? endDate : undefined,
      endOccurrences: endMode === 'after' ? endAfter : undefined,
    });
  };

  // call update whenever dependencies change
  useEffect(update, [freq, time, weeklyDays, monthlyDay, yearMonth, startDate, endMode, endDate, endAfter]);

  const toggleWeekday = (d: number) => {
    setWeeklyDays((prev) =>
      prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d],
    );
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Repeats */}
      <div className="space-y-2">
        <label className="block text-sm font-medium">Repeats every</label>
        <div className="flex gap-2 items-center">
          <Input
            type="number"
            min={1}
            value={interval}
            onChange={(e) => setInterval(Number(e.target.value))}
            className="w-20"
          />
          <Select value={freq} onChange={(e) => setFreq(e.target.value as any)} className="w-40">
            <option value="daily">Day</option>
            <option value="weekly">Week</option>
            <option value="monthly">Month</option>
            <option value="yearly">Year</option>
          </Select>
        </div>
        {freq === 'weekly' && (
          <div className="flex gap-2 pt-2">
            {weekdays.map((d) => (
              <button
                key={d.value}
                type="button"
                className={cn(
                  'h-8 w-8 rounded-md border text-sm',
                  weeklyDays.includes(d.value)
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted',
                )}
                onClick={() => toggleWeekday(d.value)}
              >
                {d.label.charAt(0)}
              </button>
            ))}
          </div>
        )}
        {freq === 'monthly' && (
          <div className="mt-2 space-y-2">
            <label className="flex items-center gap-2 text-sm">
              <Checkbox checked={monthlyMode === 'day'} onCheckedChange={() => setMonthlyMode('day')} />
              On day
              <Input
                type="number"
                min={1}
                max={31}
                value={monthlyDay}
                onChange={(e) => setMonthlyDay(Number(e.target.value))}
                className="w-20"
                disabled={monthlyMode !== 'day'}
              />
            </label>
            <label className="flex items-center gap-2 text-sm">
              <Checkbox checked={monthlyMode === 'nth'} onCheckedChange={() => setMonthlyMode('nth')} />
              <Select
                value={nthWeek}
                onChange={(e) => setNthWeek(e.target.value as any)}
                className="w-24"
                disabled={monthlyMode !== 'nth'}
              >
                <option value="1">1st</option>
                <option value="2">2nd</option>
                <option value="3">3rd</option>
                <option value="4">4th</option>
                <option value="L">Last</option>
              </Select>
              <Select
                value={nthWeekday.toString()}
                onChange={(e) => setNthWeekday(Number(e.target.value))}
                className="w-24"
                disabled={monthlyMode !== 'nth'}
              >
                {weekdays.map((d) => (
                  <option key={d.value} value={d.value}>
                    {d.label}
                  </option>
                ))}
              </Select>
            </label>
          </div>
        )}
        {freq === 'yearly' && (
          <Input
            type="text"
            placeholder="MM-DD"
            value={yearMonth}
            onChange={(e) => setYearMonth(e.target.value)}
            className="w-28 mt-2"
          />
        )}
        {/* time */}
        <Input type="time" value={time} onChange={(e) => setTime(e.target.value)} className="w-32 mt-2" />
      </div>

      {/* Starts */}
      <div>
        <label className="block text-sm font-medium">Starts</label>
        <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="w-40" />
      </div>

      {/* Ends */}
      <div className="space-y-2">
        <label className="block text-sm font-medium">Ends</label>
        <div className="flex flex-col gap-1">
          <label className="flex items-center gap-2 text-sm">
            <Checkbox checked={endMode === 'never'} onCheckedChange={() => setEndMode('never')} /> Never
          </label>
          <label className="flex items-center gap-2 text-sm">
            <Checkbox checked={endMode === 'on'} onCheckedChange={() => setEndMode('on')} />
            On
            <Input
              type="date"
              value={endDate}
              disabled={endMode !== 'on'}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-40"
            />
          </label>
          <label className="flex items-center gap-2 text-sm">
            <Checkbox checked={endMode === 'after'} onCheckedChange={() => setEndMode('after')} />
            After
            <Input
              type="number"
              min={1}
              value={endAfter}
              disabled={endMode !== 'after'}
              onChange={(e) => setEndAfter(Number(e.target.value))}
              className="w-24"
            />
            occurrences
          </label>
        </div>
      </div>
    </div>
  );
} 