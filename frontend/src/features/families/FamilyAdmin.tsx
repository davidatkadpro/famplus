import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../../lib/api';

interface Family {
  id: number;
  name: string;
  settings_json: Record<string, unknown>;
}

export default function FamilyAdmin() {
  const queryClient = useQueryClient();
  const { data: families, isLoading } = useQuery<Family[]>(
    ['families'],
    async () => {
      const res = await api.get('/families/');
      return res.data as Family[];
    },
  );

  const createFamily = useMutation(
    (name: string) => api.post('/families/', { name }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['families']);
        setNewName('');
      },
    },
  );

  const updateFamily = useMutation(
    ({ id, name }: { id: number; name: string }) =>
      api.patch(`/families/${id}/`, { name }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['families']);
        setEditFamily(null);
      },
    },
  );

  const deleteFamily = useMutation(
    (id: number) => api.delete(`/families/${id}/`),
    {
      onSuccess: () => queryClient.invalidateQueries(['families']),
    },
  );

  const [newName, setNewName] = useState('');
  const [editFamily, setEditFamily] = useState<Family | null>(null);
  const [editName, setEditName] = useState('');

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Family Administration</h1>
      <div className="mb-4 flex gap-2">
        <input
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="New family name"
          className="border px-2 py-1"
        />
        <button
          onClick={() => newName && createFamily.mutate(newName)}
          className="px-3 py-1 rounded bg-blue-500 text-white"
        >
          Add
        </button>
      </div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Name</th>
              <th className="p-2" />
            </tr>
          </thead>
          <tbody>
            {families?.map((fam) => (
              <tr key={fam.id} className="border-t">
                <td className="p-2">{fam.id}</td>
                <td className="p-2">{fam.name}</td>
                <td className="p-2 text-right space-x-2">
                  <button
                    onClick={() => {
                      setEditFamily(fam);
                      setEditName(fam.name);
                    }}
                    className="underline text-blue-600"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => deleteFamily.mutate(fam.id)}
                    className="underline text-red-600"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {editFamily && (
        <dialog
          open
          className="fixed inset-0 bg-black/50 flex items-center justify-center"
        >
          <div className="bg-white dark:bg-gray-800 p-4 rounded w-72">
            <p className="mb-2">Edit family {editFamily.name}</p>
            <input
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              className="border px-2 py-1 w-full mb-4"
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() =>
                  updateFamily.mutate({ id: editFamily.id, name: editName })
                }
                className="px-3 py-1 rounded bg-blue-500 text-white"
              >
                Save
              </button>
              <button
                onClick={() => setEditFamily(null)}
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
