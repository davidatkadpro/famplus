import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { RoleBadge } from '@/components/ui/role-badge';
import { Table } from '@/components/ui/table';
import { Select } from '@/components/ui/select';
import { ResponsiveTable } from '@/components/ui/responsive-table';

interface Family {
  id: number;
  name: string;
  settings_json: Record<string, unknown>;
}

interface Membership { id: number; user: number; role: 'parent' | 'child' | 'guest'; }

interface Invitation { id: number; email: string; role: 'parent' | 'child' | 'guest'; accepted: boolean; }

export default function FamilyAdmin() {
  const queryClient = useQueryClient();
  const {
    data: families,
    isPending: isLoading,
  } = useQuery<Family[]>({
    queryKey: ['families'],
    queryFn: async () => {
      const res = await api.get('/families/');
      return res.data as Family[];
    },
  });

  const createFamily = useMutation({
    mutationFn: (name: string) => api.post('/families/', { name }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['families'] });
      setNewName('');
    },
  });

  const updateFamily = useMutation({
    mutationFn: ({ id, name }: { id: number; name: string }) =>
      api.patch(`/families/${id}/`, { name }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['families'] });
      setEditFamily(null);
    },
  });

  const deleteFamily = useMutation({
    mutationFn: (id: number) => api.delete(`/families/${id}/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['families'] });
    },
  });

  const [newName, setNewName] = useState('');
  const [editFamily, setEditFamily] = useState<Family | null>(null);
  const [editName, setEditName] = useState('');

  const [selectedFamily, setSelectedFamily] = useState<Family | null>(null);

  const { data: members } = useQuery<Membership[]>({
    queryKey: ['members', selectedFamily?.id],
    queryFn: async () =>
      (await api.get('/family-memberships/', { params: { family: selectedFamily?.id } })).data,
    enabled: !!selectedFamily,
  });

  const { data: invites } = useQuery<Invitation[]>({
    queryKey: ['invites', selectedFamily?.id],
    queryFn: async () =>
      (await api.get('/family-invitations/', { params: { family: selectedFamily?.id } })).data,
    enabled: !!selectedFamily,
  });

  const inviteMutation = useMutation({
    mutationFn: (payload: { email: string; role: string; family: number }) =>
      api.post('/family-invitations/', payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['invites'] }),
  });

  const cancelInvite = useMutation({
    mutationFn: (id: number) => api.delete(`/family-invitations/${id}/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['invites'] }),
  });

  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<'parent' | 'child' | 'guest'>('child');

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Family Administration</h1>
      <div className="mb-4 flex gap-2">
        <Input
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="New family name"
          className="w-64"
        />
        <Button onClick={() => newName && createFamily.mutate(newName)}>Add</Button>
      </div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <ResponsiveTable
          data={families ?? []}
          columns={[
            { header: 'ID', cell: (f: Family) => f.id, mobileLabel: 'ID' },
            { header: 'Name', cell: (f: Family) => f.name },
            {
              header: '',
              cell: (f: Family) => (
                <div className="space-x-2 text-right">
                  <Button
                    variant="link"
                    onClick={() => {
                      setEditFamily(f);
                      setEditName(f.name);
                    }}
                  >
                    Edit
                  </Button>
                  <Button variant="link" onClick={() => deleteFamily.mutate(f.id)}>
                    Delete
                  </Button>
                </div>
              ),
              hideOnMobile: true,
            },
          ]}
          onRowClick={(f: Family) => setSelectedFamily(f)}
        />
      )}

      {selectedFamily && (
        <dialog open className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <Card className="w-full max-w-xl">
            <CardHeader>
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">Family: {selectedFamily.name}</h3>
                <Button variant="outline" size="sm" onClick={() => setSelectedFamily(null)}>
                  Close
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h4 className="mb-2 font-medium">Members</h4>
                <Table>
                  <thead>
                    <tr className="border-b bg-muted/50 text-muted-foreground">
                      <th className="px-2 py-1 text-left">User</th>
                      <th className="px-2 py-1 text-left">Role</th>
                    </tr>
                  </thead>
                  <tbody>
                    {members?.map((m) => (
                      <tr key={m.id} className="border-b">
                        <td className="px-2 py-1">{m.user}</td>
                        <td className="px-2 py-1">
                          <RoleBadge role={m.role} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>

              <div>
                <h4 className="mb-2 font-medium">Pending Invitations</h4>
                <Table>
                  <thead>
                    <tr className="border-b bg-muted/50 text-muted-foreground">
                      <th className="px-2 py-1 text-left">Email</th>
                      <th className="px-2 py-1 text-left">Role</th>
                      <th />
                    </tr>
                  </thead>
                  <tbody>
                    {invites
                      ?.filter((i) => !i.accepted)
                      .map((inv) => (
                        <tr key={inv.id} className="border-b">
                          <td className="px-2 py-1">{inv.email}</td>
                          <td className="px-2 py-1">
                            <RoleBadge role={inv.role} />
                          </td>
                          <td className="px-2 py-1">
                            <Button variant="link" size="sm" onClick={() => cancelInvite.mutate(inv.id)}>
                              Cancel
                            </Button>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </Table>
              </div>

              <div className="flex gap-2 items-end">
                <Input placeholder="Invite email" value={inviteEmail} onChange={(e) => setInviteEmail(e.target.value)} />
                <Select
                  value={inviteRole}
                  onChange={(e) => setInviteRole((e.target as HTMLSelectElement).value as any)}
                  className="w-32"
                >
                  <option value="parent">Parent</option>
                  <option value="child">Child</option>
                  <option value="guest">Guest</option>
                </Select>
                <Button
                  disabled={!inviteEmail}
                  onClick={() =>
                    inviteMutation.mutate({ email: inviteEmail, role: inviteRole, family: selectedFamily.id })
                  }
                >
                  Send Invite
                </Button>
              </div>
            </CardContent>
          </Card>
        </dialog>
      )}

      {editFamily && (
        <dialog open className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white dark:bg-gray-800 p-4 rounded w-72">
            <p className="mb-2">Edit family {editFamily.name}</p>
            <Input
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              className="w-full mb-4"
            />
            <div className="flex justify-end gap-2">
              <Button onClick={() => updateFamily.mutate({ id: editFamily.id, name: editName })}>
                Save
              </Button>
              <Button variant="outline" onClick={() => setEditFamily(null)}>
                Cancel
              </Button>
            </div>
          </div>
        </dialog>
      )}
    </div>
  );
}
