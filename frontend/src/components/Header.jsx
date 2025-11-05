import { Activity, TrendingUp } from 'lucide-react'

export default function Header({ summary }) {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-6">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Tech Momentum Arbitrage Engine
              </h1>
              <p className="text-sm text-gray-500">Mist Inc. Intelligence Lab</p>
            </div>
          </div>

          {summary && (
            <div className="flex items-center space-x-6">
              <div className="text-right">
                <p className="text-xs text-gray-500">IPO Window</p>
                <p className="text-sm font-semibold text-gray-900 uppercase">
                  {summary.ipo_window_health}
                </p>
              </div>
              <div className="flex items-center space-x-2 px-4 py-2 bg-green-50 rounded-lg">
                <TrendingUp className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-900">
                  {summary.high_conviction_count} High-Conviction Signals
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
