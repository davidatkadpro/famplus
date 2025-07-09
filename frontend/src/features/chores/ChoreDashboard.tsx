import React, { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { ResponsiveTable } from '@/components/ui/responsive-table';

interface Entry {
  id: number;
  chore: number;
  assigned_to: number;
  due_date: string;
  status: string;
}

interface Chore { id: number; name: string; points: number; }

export default function ChoreDashboard() {
  const queryClient = useQueryClient();

  const { data: entries, isLoading } = useQuery<Entry[]>({
    queryKey: ['chore-entries'],
    queryFn: async () => {
      const res = await api.get('/chore-entries/');
      return res.data as Entry[];
    },
  });

  const { data: chores } = useQuery<Chore[]>({
    queryKey: ['chores'],
    queryFn: async () => (await api.get('/chores/')).data,
  });

  const approveMutation = useMutation({
    mutationFn: (id: number) => api.post(`/chore-entries/${id}/approve/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['chore-entries'] }),
  });

  const rejectMutation = useMutation({
    mutationFn: (id: number) => api.post(`/chore-entries/${id}/reject/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['chore-entries'] }),
  });

  const completeMutation = useMutation({
    mutationFn: (entry: Entry) => api.patch(`/chore-entries/${entry.id}/`, { status: 'completed' }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['chore-entries'] }),
  });

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Chore Entries</h2>
          <div className="flex gap-2">
            <Input placeholder="Search" className="h-8 w-48" />
            <Button size="sm">Add</Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <p>Loading…</p>
        ) : (
          <ResponsiveTable
            data={entries ?? []}
            columns={[
              {
                header: 'Chore',
                cell: (e: Entry) =>
                  chores?.find((c) => c.id === e.chore)?.name ?? e.chore,
              },
              { header: 'Due', cell: (e: Entry) => e.due_date },
              {
                header: 'Status',
                cell: (e: Entry) => <span className="capitalize">{e.status}</span>,
              },
              {
                header: '',
                cell: (e: Entry) => (
                  <div className="flex gap-2">
                    {e.status === 'awaiting' && (
                      <Button size="sm" onClick={() => completeMutation.mutate(e)}>
                        Complete
                      </Button>
                    )}
                    {e.status === 'completed' && (
                      <>
                        <Button size="sm" onClick={() => approveMutation.mutate(e.id)}>
                          Approve
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => rejectMutation.mutate(e.id)}
                        >
                          Reject
                        </Button>
                      </>
                    )}
                  </div>
                ),
                hideOnMobile: true,
              },
            ]}
          />
        )}
      </CardContent>
    </Card>
  );
}
