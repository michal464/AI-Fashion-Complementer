export default function ResultCard({ result }) {
  if (result.error) return <p style={{ color: 'red', textAlign: 'center' }}>{result.error}</p>

  const { predicted_category, predicted_style, recommendations } = result

  return (
    <div style={{ direction: 'rtl', marginTop: 28 }}>

      {/* Summary */}
      <div style={summaryStyle}>
        <span>📦 קטגוריה: <strong>{predicted_category}</strong></span>
        <span style={{ margin: '0 16px' }}>|</span>
        <span>🎨 סגנון: <strong>{predicted_style}</strong></span>
      </div>

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 ? (
        <>
          <h3 style={{ textAlign: 'center', color: '#444', marginBottom: 16 }}>✨ פריטים משלימים מומלצים</h3>
          <div style={gridStyle}>
            {recommendations.map((item, i) => (
              <div key={i} style={cardStyle}>
                <img
                  src={`/catalog/${item.image_path}`}
                  alt={item.name}
                  style={imgStyle}
                />
                <div style={{ fontWeight: 600, fontSize: 14 }}>{item.name}</div>
                <div style={{ color: '#888', fontSize: 12, marginTop: 4 }}>{item.category} · {item.style}</div>
                <div style={scoreBadge}>{(item.score * 100).toFixed(0)}% התאמה</div>
              </div>
            ))}
          </div>
        </>
      ) : (
        <p style={{ textAlign: 'center', color: '#888' }}>
          אין פריטים בקטלוג עדיין — הרץ את generate_embeddings.py
        </p>
      )}
    </div>
  )
}

const summaryStyle = {
  textAlign: 'center',
  background: '#f0eeff',
  border: '1px solid #6c63ff',
  borderRadius: 10,
  padding: '12px 20px',
  marginBottom: 24,
  fontSize: 16,
}

const gridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
  gap: 16,
}

const cardStyle = {
  background: '#fff',
  border: '1px solid #e0dff5',
  borderRadius: 12,
  padding: '16px 12px',
  textAlign: 'center',
  boxShadow: '0 2px 10px rgba(108,99,255,0.08)',
}

const imgStyle = {
  width: '100%',
  height: 120,
  objectFit: 'cover',
  borderRadius: 8,
  marginBottom: 8,
}

const scoreBadge = {
  marginTop: 8,
  display: 'inline-block',
  background: '#6c63ff',
  color: '#fff',
  borderRadius: 20,
  padding: '2px 10px',
  fontSize: 11,
}
