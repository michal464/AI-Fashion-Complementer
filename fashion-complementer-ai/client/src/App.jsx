import { useState } from 'react'
import ImageUploader from './components/ImageUploader.jsx'
import ResultCard from './components/ResultCard.jsx'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'Arial, sans-serif', direction: 'rtl' }}>
      <h1 style={{ textAlign: 'center' }}>👗 AI Fashion Complementer</h1>
      <p style={{ textAlign: 'center', color: '#555' }}>העלה תמונה של פריט לבוש וקבל המלצת סגנון</p>

      <ImageUploader onResult={setResult} onLoading={setLoading} />

      {loading && <p style={{ textAlign: 'center', marginTop: 16 }}>⏳ מנתח תמונה...</p>}
      {result && !loading && <ResultCard result={result} />}
    </div>
  )
}
