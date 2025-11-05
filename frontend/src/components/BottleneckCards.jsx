import { AlertCircle, TrendingUp, Building2, DollarSign } from 'lucide-react'

export default function BottleneckCards({ bottlenecks }) {
  const getPriorityColor = (priority) => {
    const colors = {
      CRITICAL: 'bg-red-100 text-red-800 border-red-200',
      HIGH: 'bg-orange-100 text-orange-800 border-orange-200',
      MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    }
    return colors[priority] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  const formatMarketSize = (size) => {
    if (!size) return null
    if (size >= 1_000_000_000) return `$${(size / 1_000_000_000).toFixed(1)}B`
    return `$${(size / 1_000_000).toFixed(0)}M`
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {bottlenecks.map((bottleneck, index) => (
        <div key={index} className="card card-hover">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                {bottleneck.bottleneck_name}
              </h3>
              <div className="flex items-center space-x-2">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(bottleneck.priority)}`}>
                  {bottleneck.priority}
                </span>
                <span className="text-sm text-gray-500">
                  {bottleneck.sector}
                </span>
              </div>
            </div>
            <div className="flex items-center space-x-1 px-3 py-1 bg-blue-50 rounded-lg">
              <TrendingUp className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-semibold text-blue-900">
                {(bottleneck.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>

          {/* Description */}
          <p className="text-sm text-gray-600 mb-4 leading-relaxed">
            {bottleneck.description}
          </p>

          {/* Market Size */}
          {bottleneck.estimated_market_size && (
            <div className="flex items-center space-x-2 mb-4 p-3 bg-green-50 rounded-lg">
              <DollarSign className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium text-green-900">
                {formatMarketSize(bottleneck.estimated_market_size)} market opportunity
              </span>
            </div>
          )}

          {/* Evidence */}
          <div className="mb-4">
            <h4 className="text-xs font-medium text-gray-500 uppercase mb-2">
              Evidence
            </h4>
            <ul className="space-y-1.5">
              {bottleneck.evidence.slice(0, 3).map((evidence, i) => (
                <li key={i} className="flex items-start space-x-2 text-sm text-gray-600">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>{evidence}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Companies & Proxies */}
          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
            <div>
              <h4 className="text-xs font-medium text-gray-500 uppercase mb-2">
                Private Companies
              </h4>
              <div className="flex flex-wrap gap-1">
                {bottleneck.private_companies.slice(0, 3).map((company, i) => (
                  <span key={i} className="inline-block px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                    {company}
                  </span>
                ))}
                {bottleneck.private_companies.length > 3 && (
                  <span className="inline-block px-2 py-1 bg-gray-100 text-gray-500 rounded text-xs">
                    +{bottleneck.private_companies.length - 3}
                  </span>
                )}
              </div>
            </div>
            <div>
              <h4 className="text-xs font-medium text-gray-500 uppercase mb-2">
                Public Proxies
              </h4>
              <div className="flex flex-wrap gap-1">
                {bottleneck.public_proxies.map((proxy, i) => (
                  <span key={i} className="inline-block px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                    {proxy}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
