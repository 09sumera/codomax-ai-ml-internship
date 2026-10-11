import React, { useState, useEffect } from 'react';
import {
  IndianRupee,
  Plus,
  Trash2,
  AlertTriangle,
  CheckCircle2,
  Clock,
  RotateCcw,
  Tag,
  PieChart,
} from 'lucide-react';
import { Trip, Expense, BudgetAnalytics } from '../../types/trip';
import { tripService } from '../../services/tripService';

interface BudgetExpenseTrackerProps {
  trip: Trip;
}

const CATEGORIES = [
  { value: 'accommodation', label: 'Accommodation' },
  { value: 'transport', label: 'Transport' },
  { value: 'activities', label: 'Activities & Tours' },
  { value: 'food', label: 'Food & Dining' },
  { value: 'shopping', label: 'Shopping' },
  { value: 'emergency', label: 'Emergency & Medical' },
  { value: 'other', label: 'Other / Miscellaneous' },
] as const;

export const BudgetExpenseTracker: React.FC<BudgetExpenseTrackerProps> = ({ trip }) => {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [analytics, setAnalytics] = useState<BudgetAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // New expense form
  const [formData, setFormData] = useState({
    title: '',
    amount: '',
    category: 'activities' as Expense['category'],
    payment_status: 'paid' as Expense['payment_status'],
    date: new Date().toISOString().split('T')[0],
    notes: '',
  });

  useEffect(() => {
    loadExpenses();
  }, [trip.id]);

  const loadExpenses = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await tripService.getExpenses(trip.id);
      setExpenses(data.expenses || []);
      setAnalytics(data.analytics || null);
    } catch (err: any) {
      setError(err?.response?.data?.message || 'Failed to load trip expenses.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddExpense = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || !formData.amount) return;

    try {
      setSubmitting(true);
      const res = await tripService.addExpense(trip.id, {
        title: formData.title.trim(),
        amount: Number(formData.amount),
        category: formData.category,
        payment_status: formData.payment_status,
        currency: trip.currency || 'INR',
        date: formData.date,
        notes: formData.notes.trim() || undefined,
      });

      setExpenses((prev) => [res.expense, ...prev]);
      setAnalytics(res.analytics);
      setShowAddModal(false);
      setFormData({
        title: '',
        amount: '',
        category: 'activities',
        payment_status: 'paid',
        date: new Date().toISOString().split('T')[0],
        notes: '',
      });
    } catch (err: any) {
      alert(err?.response?.data?.message || 'Failed to record expense.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteExpense = async (expenseId: string) => {
    if (!window.confirm('Delete this expense record?')) return;
    try {
      const res = await tripService.deleteExpense(trip.id, expenseId);
      setExpenses((prev) => prev.filter((ex) => ex.id !== expenseId));
      setAnalytics(res.analytics);
    } catch (err: any) {
      alert(err?.response?.data?.message || 'Failed to delete expense.');
    }
  };

  const handleStatusChange = async (
    expenseId: string,
    newStatus: Expense['payment_status']
  ) => {
    try {
      const res = await tripService.updateExpense(trip.id, expenseId, {
        payment_status: newStatus,
      });
      setExpenses((prev) =>
        prev.map((ex) => (ex.id === expenseId ? res.expense : ex))
      );
      setAnalytics(res.analytics);
    } catch (err: any) {
      alert(err?.response?.data?.message || 'Failed to update payment status.');
    }
  };

  const currencySymbol =
    trip.currency === 'USD' ? '$' : trip.currency === 'EUR' ? '€' : '₹';

  return (
    <div className="space-y-8">
      {/* Analytics Overview Cards */}
      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Card 1: Total Budget */}
          <div className="bg-surface p-5 rounded-2xl border border-border">
            <div className="flex items-center justify-between text-xs text-muted uppercase font-semibold mb-1">
              <span>Total Budget</span>
              <IndianRupee className="w-4 h-4 text-primary" />
            </div>
            <div className="text-2xl font-bold text-text">
              {currencySymbol}
              {analytics.total_budget.toLocaleString()}
            </div>
            <div className="text-xs text-muted mt-1">Allocated for this journey</div>
          </div>

          {/* Card 2: Actual Paid Expenses */}
          <div className="bg-surface p-5 rounded-2xl border border-border">
            <div className="flex items-center justify-between text-xs text-muted uppercase font-semibold mb-1">
              <span>Actual Paid</span>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-emerald-400">
              {currencySymbol}
              {analytics.actual_paid_expenses.toLocaleString()}
            </div>
            <div className="text-xs text-muted mt-1">
              {analytics.budget_used_percentage.toFixed(1)}% of total budget used
            </div>
          </div>

          {/* Card 3: Remaining Budget or Overrun Alert */}
          <div
            className={`p-5 rounded-2xl border ${
              analytics.is_over_budget
                ? 'bg-red-500/10 border-red-500/50'
                : 'bg-surface border-border'
            }`}
          >
            <div className="flex items-center justify-between text-xs uppercase font-semibold mb-1">
              <span className={analytics.is_over_budget ? 'text-red-400' : 'text-muted'}>
                {analytics.is_over_budget ? 'Budget Overrun' : 'Remaining Budget'}
              </span>
              {analytics.is_over_budget ? (
                <AlertTriangle className="w-4 h-4 text-red-400" />
              ) : (
                <IndianRupee className="w-4 h-4 text-accent" />
              )}
            </div>
            <div
              className={`text-2xl font-bold ${
                analytics.is_over_budget ? 'text-red-400' : 'text-accent'
              }`}
            >
              {currencySymbol}
              {analytics.is_over_budget
                ? analytics.overrun_amount.toLocaleString()
                : analytics.remaining_budget.toLocaleString()}
            </div>
            <div className="text-xs text-muted mt-1">
              {analytics.is_over_budget
                ? 'Exceeded total planned budget!'
                : `${(100 - analytics.budget_used_percentage).toFixed(1)}% available funds`}
            </div>
          </div>

          {/* Card 4: Commitments & Refunds */}
          <div className="bg-surface p-5 rounded-2xl border border-border">
            <div className="flex items-center justify-between text-xs text-muted uppercase font-semibold mb-1">
              <span>Pending & Refunds</span>
              <Clock className="w-4 h-4 text-yellow-400" />
            </div>
            <div className="text-sm font-semibold text-text">
              Pending:{' '}
              <span className="text-yellow-400">
                {currencySymbol}
                {analytics.pending_commitments.toLocaleString()}
              </span>
            </div>
            <div className="text-sm font-semibold text-text mt-1">
              Refunds:{' '}
              <span className="text-sky-400">
                {currencySymbol}
                {analytics.refunded_amount.toLocaleString()}
              </span>
            </div>
            <div className="text-[11px] text-muted mt-1">
              Effective balance: {currencySymbol}
              {analytics.potential_remaining_budget.toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {/* Category Breakdown Progress Bar */}
      {analytics && Object.keys(analytics.category_breakdown).length > 0 && (
        <div className="bg-surface p-5 rounded-2xl border border-border">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-text flex items-center gap-2">
              <PieChart className="w-4 h-4 text-primary" />
              Category Spend Breakdown
            </h4>
            <span className="text-xs text-muted">
              {analytics.expense_count} recorded expenses
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {Object.entries(analytics.category_breakdown).map(([cat, summary]) => (
              <div
                key={cat}
                className="bg-background/60 p-3 rounded-xl border border-border/50 text-xs"
              >
                <div className="capitalize text-muted font-medium truncate">{cat}</div>
                <div className="text-sm font-bold text-text mt-1">
                  {currencySymbol}
                  {summary.total_paid.toLocaleString()}
                </div>
                <div className="text-[11px] text-primary mt-0.5">
                  {summary.percentage_of_budget.toFixed(1)}% of budget
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Header & Add Button */}
      <div className="flex justify-between items-center pt-2">
        <div>
          <h3 className="text-lg font-bold text-text">Logged Expenses</h3>
          <p className="text-xs text-muted">
            Track daily receipts, accommodation dues, and transportation tickets
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-1.5 bg-primary hover:bg-primary/90 text-background px-4 py-2.5 rounded-xl font-semibold text-xs shadow-md transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Add Expense</span>
        </button>
      </div>

      {/* Expenses Table / List */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-primary" />
        </div>
      ) : expenses.length === 0 ? (
        <div className="bg-surface/50 border border-border rounded-2xl p-10 text-center text-muted text-sm">
          No expenses recorded yet. Click "Add Expense" to track your real-time travel costs.
        </div>
      ) : (
        <div className="bg-surface border border-border rounded-2xl overflow-hidden shadow-sm">
          <div className="divide-y divide-border">
            {expenses.map((expense) => {
              const isPaid = expense.payment_status === 'paid';
              const isPending = expense.payment_status === 'pending';
              const isRefunded = expense.payment_status === 'refunded';

              return (
                <div
                  key={expense.id}
                  className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-background/40 transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <div
                      className={`p-2 rounded-xl mt-0.5 ${
                        isPaid
                          ? 'bg-emerald-500/10 text-emerald-400'
                          : isPending
                          ? 'bg-yellow-500/10 text-yellow-400'
                          : isRefunded
                          ? 'bg-sky-500/10 text-sky-400'
                          : 'bg-neutral-800 text-muted'
                      }`}
                    >
                      <Tag className="w-4 h-4" />
                    </div>

                    <div>
                      <div className="font-semibold text-text text-sm">{expense.title}</div>
                      <div className="flex flex-wrap items-center gap-2 text-xs text-muted mt-0.5">
                        <span className="capitalize">{expense.category}</span>
                        <span>•</span>
                        <span>{expense.date}</span>
                        {expense.notes && (
                          <>
                            <span>•</span>
                            <span className="italic truncate max-w-xs">{expense.notes}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between sm:justify-end gap-4 self-end sm:self-auto">
                    <div className="text-right">
                      <div className="font-bold text-sm text-text">
                        {currencySymbol}
                        {expense.amount.toLocaleString()}
                      </div>
                      <select
                        value={expense.payment_status}
                        onChange={(e) =>
                          handleStatusChange(
                            expense.id,
                            e.target.value as Expense['payment_status']
                          )
                        }
                        className={`text-[11px] font-semibold rounded-lg px-2 py-0.5 mt-0.5 border bg-background ${
                          isPaid
                            ? 'text-emerald-400 border-emerald-500/30'
                            : isPending
                            ? 'text-yellow-400 border-yellow-500/30'
                            : isRefunded
                            ? 'text-sky-400 border-sky-500/30'
                            : 'text-neutral-400 border-neutral-700'
                        }`}
                      >
                        <option value="paid">Paid</option>
                        <option value="pending">Pending</option>
                        <option value="refunded">Refunded</option>
                        <option value="cancelled">Cancelled</option>
                      </select>
                    </div>

                    <button
                      onClick={() => handleDeleteExpense(expense.id)}
                      className="p-1.5 text-muted hover:text-red-400 rounded-lg hover:bg-red-500/10 transition-colors"
                      title="Delete expense"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Add Expense Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-surface border border-border rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
            <h4 className="text-lg font-bold text-white mb-1">Add Trip Expense</h4>
            <p className="text-xs text-muted mb-4">
              Record a paid bill, reservation deposit, or pending commitment.
            </p>

            <form onSubmit={handleAddExpense} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-1">
                  Expense Description *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Scuba diving pass, Dinner at Sea View, Train fare"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full bg-background border border-border rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-primary"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-1">
                    Amount ({currencySymbol}) *
                  </label>
                  <input
                    type="number"
                    min="1"
                    step="1"
                    required
                    placeholder="e.g. 2500"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    className="w-full bg-background border border-border rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-1">
                    Category
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        category: e.target.value as Expense['category'],
                      })
                    }
                    className="w-full bg-background border border-border rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-primary"
                  >
                    {CATEGORIES.map((cat) => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-1">
                    Payment Status
                  </label>
                  <select
                    value={formData.payment_status}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        payment_status: e.target.value as Expense['payment_status'],
                      })
                    }
                    className="w-full bg-background border border-border rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-primary"
                  >
                    <option value="paid">Paid</option>
                    <option value="pending">Pending</option>
                    <option value="refunded">Refunded</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-1">
                    Date
                  </label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                    className="w-full bg-background border border-border rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-primary"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-1">
                  Notes (Optional)
                </label>
                <input
                  type="text"
                  placeholder="e.g. Receipt #1248, paid via Google Pay"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full bg-background border border-border rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-primary"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-sm font-medium text-muted hover:text-white border border-border"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2 rounded-xl text-sm font-semibold bg-primary hover:bg-primary/90 text-background transition-colors disabled:opacity-50"
                >
                  {submitting ? 'Saving...' : 'Save Expense'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
