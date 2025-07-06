import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../../lib/api';

interface Entry {
  id: number;
  chore: number;
  assigned_to: number;
  due_date: string;
  status: string;
}

export default function ChoreDashboard() {
  const queryClient = useQueryClient();

  const { data: entries, isLoading } = useQuery<Entry[]>(
    ['chore-entries'],
    async () => {
      const res = await api.get('/chore-entries/');
      return res.data as Entry[];
    },
  );

  const approveMutation = useMutation(
    (id: number) => api.post(`/chore-entries/${id}/approve/`),
    {
      onSuccess: () => queryClient.invalidateQueries(['chore-entries']),
    },
  );

  const [selected, setSelected] = useState<Entry | null>(null);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Chore Dashboard</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Chore</th>
              <th className="p-2 text-left">Due Date</th>
              <th className="p-2 text-left">Status</th>
              <th className="p-2" />
            </tr>
          </thead>
          <tbody>
            {entries?.map((e) => (
              <tr key={e.id} className="border-t">
                <td className="p-2">{e.id}</td>
                <td className="p-2">{e.chore}</td>
                <td className="p-2">{e.due_date}</td>
                <td className="p-2 capitalize">{e.status}</td>
                <td className="p-2 text-right">
                  {e.status === 'completed' && (
                    <button
                      onClick={() => setSelected(e)}
                      className="text-blue-600 underline"
                    >
                      Approve
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {selected && (
        <dialog
          open
          className="fixed inset-0 bg-black/50 flex items-center justify-center"
        >
          <div className="bg-white dark:bg-gray-800 p-4 rounded w-64">
            <p className="mb-4">Approve entry #{selected.id}?</p>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => {
                  approveMutation.mutate(selected.id);
                  setSelected(null);
                }}
                className="px-3 py-1 rounded bg-blue-500 text-white"
              >
                Approve
              </button>
              <button
                onClick={() => setSelected(null)}
                className="px-3 py-1 rounded border"
              >
                Cancel
              </button>
            </div>
          </div>
        </dialog>
      )}
    </div>
  );
}
