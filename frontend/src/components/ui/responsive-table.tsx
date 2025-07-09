import { Table } from '@/components/ui/table';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';
import * as React from 'react';

interface Column<T> {
  /** Header label shown in table */
  header: React.ReactNode;
  /** Render function for cell */
  cell: (row: T) => React.ReactNode;
  /** Optional label used on mobile card */
  mobileLabel?: string;
  /** Hide this column on mobile card (header still shows in table) */
  hideOnMobile?: boolean;
}

interface ResponsiveTableProps<T> {
  data: T[];
  columns: Column<T>[];
  /** unique id accessor, defaults to index */
  getRowId?: (row: T, index: number) => React.Key;
  /** Show checkbox column */
  selectable?: boolean;
  /** Callback when row checkbox changes */
  onSelectChange?: (row: T, checked: boolean) => void;
  /** Render actions/menu on far right */
  actions?: (row: T) => React.ReactNode;
  /** Additional className for wrapper */
  className?: string;
  /** Optional row click handler */
  onRowClick?: (row: T) => void;
}

export function ResponsiveTable<T>(props: ResponsiveTableProps<T>) {
  const {
    data,
    columns,
    getRowId = (_, i) => i,
    selectable,
    onSelectChange,
    actions,
    className,
    onRowClick,
  } = props;

  return (
    <div className={cn('w-full', className)}>
      {/* Desktop / Tablet */}
      <div className="hidden sm:block">
        <Table>
          <thead>
            <tr className="border-b bg-muted/50 text-muted-foreground">
              {selectable && <th className="p-2 w-8" />}
              {columns.map((col, idx) => (
                <th key={idx} className="px-2 py-1 text-left">
                  {col.header}
                </th>
              ))}
              {actions && <th className="p-2 w-8" />}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => {
              const id = getRowId(row, idx);
              return (
                <tr
                  key={id}
                  className={cn('border-t', onRowClick && 'cursor-pointer hover:bg-accent/20')}
                  onClick={() => onRowClick?.(row)}
                >
                  {selectable && (
                    <td className="p-2">
                      <Checkbox
                        onCheckedChange={(checked) =>
                          onSelectChange?.(row, !!checked)
                        }
                      />
                    </td>
                  )}
                  {columns.map((col, ci) => (
                    <td key={ci} className="px-2 py-1">
                      {col.cell(row)}
                    </td>
                  ))}
                  {actions && <td className="p-2">{actions(row)}</td>}
                </tr>
              );
            })}
          </tbody>
        </Table>
      </div>

      {/* Mobile cards */}
      <div className="space-y-2 sm:hidden">
        {data.map((row, idx) => {
          const id = getRowId(row, idx);
          const [open, setOpen] = React.useState(false);
          return (
            <div
              key={id}
              className="rounded-lg border bg-card text-card-foreground shadow-sm"
            >
              <div
                className="flex items-center gap-2 p-3 cursor-pointer"
                onClick={() => {
                  setOpen((p) => !p);
                  onRowClick?.(row);
                }}
              >
                {selectable && (
                  <Checkbox
                    onClick={(e) => e.stopPropagation()}
                    onCheckedChange={(checked) =>
                      onSelectChange?.(row, !!checked)
                    }
                  />
                )}
                <div className="flex-1">
                  <p className="font-medium leading-none">
                    {columns[0].cell(row)}
                  </p>
                  {columns[1] && (
                    <p className="text-sm text-muted-foreground">
                      {columns[1].cell(row)}
                    </p>
                  )}
                </div>
                {actions && (
                  <div onClick={(e) => e.stopPropagation()}>{actions(row)}</div>
                )}
              </div>
              {open && (
                <div className="border-t p-3 space-y-1 text-sm">
                  {columns.slice(selectable ? 0 : 0).map((col, ci) => {
                    if (ci < 2) return null; // first two are shown already
                    if (col.hideOnMobile) return null;
                    return (
                      <div key={ci} className="flex justify-between gap-4">
                        <span className="text-muted-foreground">
                          {col.mobileLabel ?? col.header}
                        </span>
                        <span>{col.cell(row)}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
} 