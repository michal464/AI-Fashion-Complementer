import { useState, useRef } from 'react'

export default function ImageUploader({ onResult, onLoading }) {
  const [preview, setPreview] = useState(null)
  const inputRef = useRef()

  const handleFile = (file) => {
    if (!file) return
    setPreview(URL.createObjectURL(file))
    uploadImage(file)
  }

  const uploadImage = async (file) => {
    onLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/recommend', { method: 'POST', body: formData })
      const data = await res.json()
      onResult(data)
    } catch {
      onResult({ error: 'שגיאה בחיבור לשרת' })
    } finally {
      onLoading(false)
    }
  }

  return (
    <div style={{ textAlign: 'center' }}>
      {preview && (
        <img src={preview} alt="תצוגה מקדימה" style={{ maxWidth: 300, borderRadius: 12, marginBottom: 16, boxShadow: '0 4px 20px rgba(0,0,0,0.15)' }} />
      )}
      <br />
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={(e) => handleFile(e.target.files[0])}
      />
      <button onClick={() => inputRef.current.click()} style={btnStyle}>
        📸 העלה תמונה
      </button>
    </div>
  )
}

const btnStyle = {
  padding: '12px 28px',
  fontSize: 16,
  borderRadius: 8,
  border: 'none',
  background: '#6c63ff',
  color: '#fff',
  cursor: 'pointer',
}
