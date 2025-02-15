/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import { useState, useEffect } from 'react';
import { Search, ArrowUpDown } from 'lucide-react';
import { Input } from './input';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './table';
import { Button } from './button';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from './pagination';
import { useDebounce } from '@/hooks/use-debounce';

// Reuse existing Column type
interface Column<T> {
  key: keyof T;
  title: string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
  className?: string;
}

interface DataTablePaginationProps<T> {
  columns: Column<T>[];
  data: T[];
  total: number;
  pageSize?: number;
  currentPage: number;
  sortKey?: string;
  sortOrder?: 'asc' | 'desc';
  searchable?: boolean;
  onPageChange: (page: number) => void;
  onSort?: (key: string, order: 'asc' | 'desc') => void;
  onSearch?: (value: string) => void;
}

export function DataTablePagination<T extends Record<string, any>>({
  columns,
  data,
  total,
  pageSize = 10,
  currentPage,
  sortKey,
  sortOrder = 'asc',
  searchable = false,
  onPageChange,
  onSort,
  onSearch,
}: DataTablePaginationProps<T>) {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 1000); // 1s delay

  useEffect(() => {
    if (onSearch) {
      onSearch(debouncedSearchTerm);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedSearchTerm]);

  const handleSort = (key: string) => {
    if (!onSort) return;

    const newOrder = key === sortKey
      ? sortOrder === 'asc' ? 'desc' : 'asc'
      : 'asc';

    onSort(key, newOrder);
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="space-y-4 mt-2">
      {/* Search */}
      {searchable && onSearch && (
        <div className="flex items-center gap-2">
          <Search className="h-4 w-4 text-slate-400" />
          <Input
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="max-w-sm"
          />
        </div>
      )}

      {/* Table */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              {columns.map((column) => (
                <TableHead
                  key={String(column.key)}
                  className={column.className}
                >
                  {column.sortable && onSort ? (
                    <Button
                      variant="ghost"
                      onClick={() => handleSort(String(column.key))}
                      className="flex items-center gap-1 hover:bg-transparent"
                    >
                      {column.title}
                      <ArrowUpDown className={`h-4 w-4 ${sortKey === column.key ? 'opacity-100' : 'opacity-50'
                        }`} />
                    </Button>
                  ) : (
                    column.title
                  )}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            ) : (
              data.map((row, index) => (
                <TableRow key={index}>
                  {columns.map((column) => (
                    <TableCell
                      key={String(column.key)}
                      className={column.className}
                    >
                      {column.render
                        ? column.render(row[column.key], row)
                        : row[column.key]}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-600">
            Showing {data.length > 0 ? ((currentPage - 1) * pageSize) + 1 : 0} to {Math.min(currentPage * pageSize, total)} of {total} results
          </p>
        </div>
        <div>
          <Pagination>
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                  onClick={() => onPageChange(currentPage - 1)}
                  className={currentPage <= 1 ? "disabled" : ""}

                />
              </PaginationItem>
              <PaginationItem>
                <PaginationNext
                  onClick={() => onPageChange(currentPage + 1)}
                  className={currentPage >= totalPages ? "disabled" : ""}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </div>
    </div>
  );
}