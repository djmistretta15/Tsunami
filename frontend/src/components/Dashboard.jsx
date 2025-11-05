import StatCards from './StatCards'
import SignalsTable from './SignalsTable'
import BottleneckCards from './BottleneckCards'
import BacktestCard from './BacktestCard'

export default function Dashboard({ summary, signals, bottlenecks, heatmap, backtest }) {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Stats Overview */}
      <StatCards summary={summary} backtest={backtest} />

      {/* Main Content Grid */}
      <div className="mt-8 space-y-8">
        {/* Top 10 Signals */}
        <section>
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Top 10 Momentum Plays</h2>
            <p className="text-sm text-gray-500 mt-1">
              Ranked by conviction score · {signals.length} signals analyzed
            </p>
          </div>
          <SignalsTable signals={signals} />
        </section>

        {/* Emerging Bottlenecks */}
        <section>
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Emerging Bottlenecks</h2>
            <p className="text-sm text-gray-500 mt-1">
              Wave 1 infrastructure opportunities · Autonomous discovery
            </p>
          </div>
          <BottleneckCards bottlenecks={bottlenecks} />
        </section>

        {/* Backtest Results */}
        {backtest && (
          <section>
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Historical Performance</h2>
              <p className="text-sm text-gray-500 mt-1">
                Q4 2022 → Q4 2024 · Strategy validation
              </p>
            </div>
            <BacktestCard backtest={backtest} />
          </section>
        )}
      </div>
    </main>
  )
}
