import { useState } from 'react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Sparkles, Utensils, Loader2 } from 'lucide-react'
import { queryNutritionAI, type AIQueryResponse } from '@/lib/api'

export function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AIQueryResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = query.trim()
    if (!trimmed) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await queryNutritionAI(trimmed)
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-lg border border-border">
        <CardHeader className="text-center space-y-1">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary mb-2">
            <Utensils className="h-6 w-6" />
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">NutriAI</CardTitle>
          <CardDescription>
            Ask any nutrition or diet question to get AI-powered insights.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Input
                type="text"
                placeholder="e.g. How much protein is in chicken breast?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
                className="w-full"
              />
            </div>
            <Button type="submit" className="w-full cursor-pointer" disabled={loading}>
              {loading ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Sparkles className="mr-2 h-4 w-4" />
              )}
              {loading ? 'Analyzing...' : 'Analyze Nutrition'}
            </Button>
          </form>

          {error && (
            <div className="mt-4 rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-700">
              <span className="font-semibold">Error: </span>
              {error}
            </div>
          )}

          {result && (
            <div className="mt-4 space-y-3">
              <div className="rounded-md border border-border bg-muted/40 p-3 text-sm">
                <span className="font-semibold text-foreground">Query: </span>
                <span className="text-muted-foreground">{result.query}</span>
              </div>

              <div className="rounded-md border border-border bg-muted/40 p-3 text-sm space-y-2">
                <div className="font-semibold text-foreground">Response:</div>
                {typeof result.response === 'string' ? (
                  <p className="text-muted-foreground">{result.response}</p>
                ) : (
                  <pre className="text-xs text-muted-foreground whitespace-pre-wrap overflow-auto">
                    {JSON.stringify(result.response, null, 2)}
                  </pre>
                )}
              </div>

              {result.reasoning && (
                <div className="rounded-md border border-border bg-muted/40 p-3 text-sm">
                  <span className="font-semibold text-foreground">Reasoning: </span>
                  <span className="text-muted-foreground">{result.reasoning}</span>
                </div>
              )}

              {result.confidence != null && (
                <div className="rounded-md border border-border bg-muted/40 p-3 text-sm">
                  <span className="font-semibold text-foreground">Confidence: </span>
                  <span className="text-muted-foreground">
                    {(result.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default App
