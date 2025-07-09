import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ResponsiveTable } from '@/components/ui/responsive-table';
import { Select } from '@/components/ui/select';
import { DialogRoot, DialogContent, DialogClose } from '@/components/ui/dialog';
import { Scheduler, ScheduleValue } from '@/components/ui/scheduler';

interface Chore {
  id: number;
  name: string;
  points: number;
  assigned_to: number | null;
  schedule: string;
}

interface Member {
  id: number;
  user: number;
  role: 'parent' | 'child' | 'guest';
}

const today = new Date().toISOString().slice(0, 10);

export function ChoresAdmin() {
  const qc = useQueryClient();
  const [filter, setFilter] = useState<number | 'all'>('all');
  const [name, setName] = useState('');
  const [points, setPoints] = useState('');
  const [schedule, setSchedule] = useState<ScheduleValue>({
    cron: '0 8 * * *',
    startDate: today,
    endMode: 'never',
  });
  const [assignee, setAssignee] = useState<number | ''>('');
  const [open, setOpen] = useState(false);

  const { data: members } = useQuery<Member[]>({
    queryKey: ['members'],
    queryFn: async () => (await api.get('/family-memberships/')).data,
  });

  const { data: chores, isLoading } = useQuery<Chore[]>({
    queryKey: ['chores-admin', filter],
    queryFn: async () => {
      const params = filter === 'all' ? {} : { assigned_to: filter };
      return (await api.get('/chores/', { params })).data;
    },
  });

  const addChore = useMutation({
    mutationFn: () =>
      api.post('/chores/', {
        name,
        points,
        assigned_to: assignee || null,
        schedule: schedule.cron,
        start_date: schedule.startDate,
        end_mode: schedule.endMode,
        end_date: schedule.endDate,
        end_after: schedule.endOccurrences,
      }),
    onSuccess: () => {
      setName('');
      setPoints('');
      setAssignee('');
      qc.invalidateQueries({ queryKey: ['chores-admin'] });
    },
  });

  const deleteChore = useMutation({
    mutationFn: (id: number) => api.delete(`/chores/${id}/`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['chores-admin'] }),
  });

  return (
    <div className="space-y-4">
      <Button variant="secondary" onClick={() => setOpen(true)}>
        New Chore
      </Button>

      <DialogRoot open={open} onOpenChange={setOpen}>
        <DialogContent>
          <h2 className="mb-4 text-lg font-semibold">New Chore</h2>
          <div className="space-y-4">
            <Input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <Input
              placeholder="Points"
              value={points}
              onChange={(e) => setPoints(e.target.value)}
              className="w-32"
            />
            <Select
              value={assignee.toString()}
              onChange={(e) => setAssignee(Number((e.target as HTMLSelectElement).value))}
              className="w-full"
            >
              <option value="">Unassigned</option>
              {members?.map((m) => (
                <option key={m.id} value={m.user}>
                  {m.user}
                </option>
              ))}
            </Select>

            <Scheduler value={schedule} onChange={setSchedule} />

            <div className="flex justify-end gap-2 pt-4">
              <DialogClose asChild>
                <Button variant="outline">Cancel</Button>
              </DialogClose>
              <Button
                onClick={() => {
                  addChore.mutate();
                  setOpen(false);
                }}
                disabled={!name || !points || !schedule.cron}
              >
                Save
              </Button>
            </div>
          </div>
        </DialogContent>
      </DialogRoot>

      <div>
        <label className="mr-2">Filter:</label>
        <Select
          value={filter.toString()}
          onChange={(e) =>
            setFilter(
              (e.target as HTMLSelectElement).value === 'all'
                ? 'all'
                : Number((e.target as HTMLSelectElement).value),
            )
          }
          className="w-40"
        >
          <option value="all">All</option>
          {members?.map((m) => (
            <option key={m.id} value={m.user}>
              {m.user}
            </option>
          ))}
        </Select>
      </div>

      {isLoading ? (
        <p>Loading…</p>
      ) : (
        <ResponsiveTable
          data={chores ?? []}
          columns={[
            { header: 'Name', cell: (c: Chore) => c.name },
            { header: 'Points', cell: (c: Chore) => c.points },
            { header: 'Schedule', cell: (c: Chore) => c.schedule },
            {
              header: 'Assigned',
              cell: (c: Chore) => c.assigned_to ?? '—',
            },
            {
              header: '',
              cell: (c: Chore) => (
                <Button variant="link" size="sm" onClick={() => deleteChore.mutate(c.id)}>
                  Delete
                </Button>
              ),
              hideOnMobile: true,
            },
          ]}
        />
      )}
    </div>
  );
} 