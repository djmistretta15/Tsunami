import { TrendingUp, Target, Award, Zap } from 'lucide-react'

export default function StatCards({ summary, backtest }) {
  if (!summary) return null

  const stats = [
    {
      label: 'Signals Generated',
      value: summary.signals_generated,
      icon: Zap,
      color: 'blue',
    },
    {
      label: 'High Conviction',
      value: summary.high_conviction_count,
      icon: Target,
      color: 'green',
      subtitle: `${((summary.high_conviction_count / summary.signals_generated) * 100).toFixed(0)}% of total`,
    },
    {
      label: 'Avg Momentum',
      value: summary.average_momentum_score.toFixed(1),
      icon: TrendingUp,
      color: 'purple',
      suffix: '/100',
    },
    {
      label: 'Historical Alpha',
      value: backtest ? `+${(backtest.alpha_vs_qqq * 100).toFixed(0)}%` : '—',
      icon: Award,
      color: 'amber',
      subtitle: backtest ? `${(backtest.win_rate * 100).toFixed(0)}% win rate` : '',
    },
  ]

  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    amber: 'bg-amber-50 text-amber-600',
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <div key={index} className="stat-card">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-sm text-gray-500 font-medium">{stat.label}</p>
              <div className="flex items-baseline mt-2">
                <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                {stat.suffix && (
                  <span className="ml-1 text-lg text-gray-500">{stat.suffix}</span>
                )}
              </div>
              {stat.subtitle && (
                <p className="text-xs text-gray-500 mt-1">{stat.subtitle}</p>
              )}
            </div>
            <div className={`p-3 rounded-lg ${colorClasses[stat.color]}`}>
              <stat.icon className="w-6 h-6" />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
