import { TrendingUp, Award, AlertTriangle, Target } from 'lucide-react'

export default function BacktestCard({ backtest }) {
  const metrics = [
    {
      label: 'Total Return',
      value: `+${(backtest.total_return * 100).toFixed(1)}%`,
      icon: TrendingUp,
      color: 'green',
    },
    {
      label: 'Alpha vs QQQ',
      value: `+${(backtest.alpha_vs_qqq * 100).toFixed(1)}%`,
      icon: Award,
      color: 'blue',
    },
    {
      label: 'Sharpe Ratio',
      value: backtest.sharpe_ratio.toFixed(2),
      icon: Target,
      color: 'purple',
    },
    {
      label: 'Win Rate',
      value: `${(backtest.win_rate * 100).toFixed(1)}%`,
      icon: Target,
      color: 'amber',
    },
  ]

  const colorClasses = {
    green: 'text-green-600',
    blue: 'text-blue-600',
    purple: 'text-purple-600',
    amber: 'text-amber-600',
  }

  return (
    <div className="card">
      {/* Period */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Backtest Period</h3>
        <p className="text-lg font-semibold text-gray-900">
          Q4 2022 → Q4 2024
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {metrics.map((metric, index) => (
          <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
            <metric.icon className={`w-5 h-5 ${colorClasses[metric.color]} mx-auto mb-2`} />
            <div className={`text-2xl font-bold ${colorClasses[metric.color]}`}>
              {metric.value}
            </div>
            <div className="text-xs text-gray-500 mt-1">{metric.label}</div>
          </div>
        ))}
      </div>

      {/* Best Signals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            <TrendingUp className="w-4 h-4 text-green-600 mr-2" />
            Best Signals
          </h4>
          <div className="space-y-2">
            {backtest.best_signals.map((signal, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <div className="font-medium text-green-900">{signal.ticker}</div>
                  <div className="text-xs text-green-700">{signal.thesis.substring(0, 40)}...</div>
                </div>
                <div className="text-lg font-bold text-green-600">
                  +{(signal.return * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            <AlertTriangle className="w-4 h-4 text-red-600 mr-2" />
            Lessons Learned
          </h4>
          <div className="space-y-2">
            {backtest.worst_signals.map((signal, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <div>
                  <div className="font-medium text-red-900">{signal.ticker}</div>
                  <div className="text-xs text-red-700">{signal.thesis.substring(0, 40)}...</div>
                </div>
                <div className="text-lg font-bold text-red-600">
                  {(signal.return * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
