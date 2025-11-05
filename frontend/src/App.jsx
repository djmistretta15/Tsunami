import { useState, useEffect } from 'react'
import axios from 'axios'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import './App.css'

const API_URL = 'http://localhost:5000/api'

function App() {
  const [summary, setSummary] = useState(null)
  const [signals, setSignals] = useState([])
  const [bottlenecks, setBottlenecks] = useState([])
  const [heatmap, setHeatmap] = useState({})
  const [backtest, setBacktest] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [summaryRes, signalsRes, bottlenecksRes, heatmapRes, backtestRes] = await Promise.all([
        axios.get(`${API_URL}/summary`),
        axios.get(`${API_URL}/signals`),
        axios.get(`${API_URL}/bottlenecks`),
        axios.get(`${API_URL}/heatmap`),
        axios.get(`${API_URL}/backtest`),
      ])

      setSummary(summaryRes.data)
      setSignals(signalsRes.data)
      setBottlenecks(bottlenecksRes.data)
      setHeatmap(heatmapRes.data)
      setBacktest(backtestRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Loading intelligence data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header summary={summary} />
      <Dashboard
        summary={summary}
        signals={signals}
        bottlenecks={bottlenecks}
        heatmap={heatmap}
        backtest={backtest}
      />
    </div>
  )
}

export default App
