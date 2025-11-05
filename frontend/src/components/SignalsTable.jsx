import { ArrowUpRight, TrendingUp, Shield, Sparkles } from 'lucide-react'

export default function SignalsTable({ signals }) {
  const getConvictionColor = (conviction) => {
    if (conviction >= 0.80) return 'text-green-600 bg-green-50'
    if (conviction >= 0.70) return 'text-blue-600 bg-blue-50'
    return 'text-gray-600 bg-gray-50'
  }

  const getRecommendationBadge = (rec) => {
    const styles = {
      STRONG_BUY: 'bg-green-100 text-green-800',
      BUY: 'bg-blue-100 text-blue-800',
      HOLD: 'bg-yellow-100 text-yellow-800',
    }
    return styles[rec] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="card p-0 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Company
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Momentum
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Hype / Build
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Moat
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Conviction
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Action
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {signals.map((signal, index) => (
              <tr
                key={signal.company_id}
                className="hover:bg-gray-50 transition-colors cursor-pointer"
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-8 w-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                      {signal.rank}
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {signal.company}
                      </div>
                      <div className="text-xs text-gray-500">{signal.sector}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg font-semibold text-gray-900">
                          {signal.momentum_score.toFixed(1)}
                        </span>
                        <span className="text-xs text-gray-400">/100</span>
                      </div>
                      <div className="mt-1 w-24 bg-gray-200 rounded-full h-1.5">
                        <div
                          className="bg-blue-600 h-1.5 rounded-full"
                          style={{ width: `${signal.momentum_score}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center space-x-3">
                    <div className="text-center">
                      <div className="text-xs text-gray-500">Hype</div>
                      <div className="text-sm font-medium text-gray-700">
                        {signal.hype_score.toFixed(0)}
                      </div>
                    </div>
                    <div className="text-gray-300">/</div>
                    <div className="text-center">
                      <div className="text-xs text-gray-500">Build</div>
                      <div className="text-sm font-medium text-gray-700">
                        {signal.build_score.toFixed(0)}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center space-x-1">
                    <Shield className="w-4 h-4 text-gray-400" />
                    <span className="text-sm font-medium text-gray-700">
                      {signal.moat_score.toFixed(0)}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`inline-flex items-center px-3 py-1 rounded-full font-semibold text-sm ${getConvictionColor(signal.conviction)}`}>
                    <Sparkles className="w-3 h-3 mr-1" />
                    {(signal.conviction * 100).toFixed(0)}%
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getRecommendationBadge(signal.recommendation)}`}>
                    {signal.recommendation.replace('_', ' ')}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
