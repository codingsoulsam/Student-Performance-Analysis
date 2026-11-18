import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from src.predict import predict_single

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Academic Risk Predictor</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #131b2e;
      --card-border: #1f2d4d;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --danger: #ef4444;
      --success: #10b981;
      --warning: #f59e0b;
      --text-main: #f3f4f6;
      --text-sub: #9ca3af;
      --input-bg: #0d1424;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
    body {
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: var(--card-bg);
      border-bottom: 1px solid var(--card-border);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo-area { display: flex; align-items: center; gap: 10px; }
    .logo-badge {
      background: var(--primary);
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      font-weight: 800;
      font-size: 16px;
    }
    .logo-text h1 { font-size: 16px; font-weight: 700; }
    .logo-text p { font-size: 11px; color: var(--text-sub); }

    .tag-live {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11.5px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dot { width: 6px; height: 6px; background: #34d399; border-radius: 50%; }

    .container {
      max-width: 1140px;
      margin: 20px auto;
      padding: 0 16px;
      width: 100%;
      flex: 1;
    }

    .top-banner {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(139, 92, 246, 0.08));
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 18px;
    }
    .top-banner h2 { font-size: 16px; font-weight: 700; margin-bottom: 4px; color: #fff; }
    .top-banner p { font-size: 12.5px; color: var(--text-sub); line-height: 1.4; }

    .main-grid {
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 18px;
      align-items: start;
    }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
    }

    .card-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--card-border);
    }
    .card-title {
      font-size: 15px;
      font-weight: 700;
    }

    .btn-toggle-analytics {
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.35);
      color: #60a5fa;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-toggle-analytics:hover {
      background: var(--primary);
      color: #fff;
    }

    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    .form-group { display: flex; flex-direction: column; gap: 4px; }
    
    label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-sub);
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    input, select {
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      border-radius: 6px;
      padding: 8px 10px;
      color: #fff;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }
    input:focus, select:focus {
      border-color: var(--primary);
    }
    select option { background: #131b2e; color: #fff; }

    .btn-submit {
      background: var(--primary);
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 11px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      width: 100%;
      margin-top: 14px;
      transition: background 0.2s;
    }
    .btn-submit:hover { background: var(--primary-hover); }

    /* Result Box Styling */
    .result-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      min-height: 240px;
      color: var(--text-sub);
      font-size: 13px;
    }
    .result-placeholder svg {
      width: 38px;
      height: 38px;
      margin-bottom: 10px;
      opacity: 0.4;
    }

    .result-content {
      display: none;
      text-align: center;
    }

    .score-circle {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      margin: 6px auto 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
    }
    .score-risk {
      background: rgba(239, 68, 68, 0.15);
      border: 3px solid var(--danger);
      color: #f87171;
    }
    .score-safe {
      background: rgba(16, 185, 129, 0.15);
      border: 3px solid var(--success);
      color: #34d399;
    }

    .status-badge {
      display: inline-block;
      padding: 5px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      margin-bottom: 10px;
    }
    .badge-risk { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-safe { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }

    .summary-text {
      font-size: 12.5px;
      color: var(--text-main);
      line-height: 1.4;
      margin-bottom: 12px;
    }

    .suggestions {
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      border-radius: 6px;
      padding: 10px 12px;
      text-align: left;
      font-size: 12px;
      line-height: 1.5;
      color: var(--text-sub);
    }
    .suggestions b { color: #fff; }

    /* Compact Visual Analytics Section */
    .analytics-panel {
      margin-top: 20px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px 20px;
      display: none;
    }
    .analytics-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 14px;
    }
    .chart-box {
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
    }
    .chart-title {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .chart-container-fixed {
      position: relative;
      height: 180px;
      width: 100%;
      max-height: 180px;
    }
    .chart-desc {
      font-size: 11px;
      color: var(--text-sub);
      margin-top: 6px;
      line-height: 1.3;
    }
  </style>
</head>
<body>

  <header>
    <div class="logo-area">
      <div class="logo-badge">SR</div>
      <div class="logo-text">
        <h1>Student Academic Risk Predictor</h1>
        <p>Performance & Retention Evaluation Engine</p>
      </div>
    </div>
    <div class="tag-live">
      <div class="dot"></div> Model Active
    </div>
  </header>

  <div class="container">
    
    <div class="top-banner">
      <h2>Check Semester Risk &amp; Academic Standing</h2>
      <p>Enter your actual academic parameters below. The system evaluates active backlogs, attendance threshold, internal assessment scores, and study routine to calculate semester passing probability.</p>
    </div>

    <div class="main-grid">
      
      <!-- Input Form -->
      <div class="card">
        <div class="card-title-row">
          <div class="card-title">Academic Parameters (Student Information)</div>
        </div>

        <form id="studentForm" onsubmit="handlePrediction(event)">
          <div class="form-grid">
            
            <div class="form-group">
              <label>Current Attendance (%)</label>
              <input type="number" id="attendance" min="0" max="100" value="78" required>
            </div>

            <div class="form-group">
              <label>Active Backlogs / KT Count</label>
              <select id="backlogs" required>
                <option value="0" selected>0 Backlogs (All Clear)</option>
                <option value="1">1 Active Backlog</option>
                <option value="2">2 Active Backlogs</option>
                <option value="3">3 or More Backlogs</option>
              </select>
            </div>

            <div class="form-group">
              <label>Mid-Term / Internal Marks (%)</label>
              <input type="number" id="internals" min="0" max="100" value="62" required>
            </div>

            <div class="form-group">
              <label>Previous Semester SGPA (1-10)</label>
              <input type="number" id="prev_sgpa" step="0.1" min="1.0" max="10.0" value="6.8" required>
            </div>

            <div class="form-group">
              <label>Daily Self-Study Hours</label>
              <select id="study_hours" required>
                <option value="0.5">&lt; 1 hour / day</option>
                <option value="1.5" selected>1 to 2 hours / day</option>
                <option value="3.0">2.5 to 4 hours / day</option>
                <option value="5.0">&gt; 4 hours / day</option>
              </select>
            </div>

            <div class="form-group">
              <label>Assignments &amp; Labs Submitted?</label>
              <select id="assignments" required>
                <option value="yes" selected>Yes &mdash; All On Time</option>
                <option value="no">No &mdash; Pending / Defaulter</option>
              </select>
            </div>

          </div>

          <button type="submit" class="btn-submit" id="btnCheck">Calculate Academic Risk</button>
        </form>
      </div>

      <!-- Result Panel -->
      <div class="card">
        <div class="card-title-row">
          <div class="card-title">Prediction Result</div>
          <button id="btnToggleAnalytics" class="btn-toggle-analytics" style="display: none;" onclick="toggleAnalytics()">
            <span>📊</span> View Graphs
          </button>
        </div>

        <div id="placeholderView" class="result-placeholder">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p>Fill in your academic marks and attendance above to calculate live semester risk.</p>
        </div>

        <div id="resultView" class="result-content">
          <div id="riskScoreCircle" class="score-circle">--%</div>
          <div id="riskBadge" class="status-badge">--</div>
          <p id="summaryText" class="summary-text"></p>
          <div class="suggestions" id="suggestionsBox"></div>
        </div>

      </div>

    </div>

    <!-- Meaningful Student Visual Analytics Section -->
    <div id="analyticsPanel" class="analytics-panel">
      <div class="card-title-row">
        <div>
          <div class="card-title">📊 Diagnostic Breakdown &amp; Performance Comparison</div>
          <p style="font-size: 11.5px; color: var(--text-sub); margin-top: 2px;">Visualizing where your risk score comes from and how you compare against the passing benchmark</p>
        </div>
      </div>

      <div class="analytics-grid">
        
        <!-- Graph 1: Feature-wise Risk Contribution -->
        <div class="chart-box">
          <div class="chart-title">
            <span>Risk Factor Contribution (%)</span>
            <span style="font-size: 11px; color: #ef4444; font-weight: 600;">Key Bottlenecks</span>
          </div>
          <div class="chart-container-fixed">
            <canvas id="breakdownChart"></canvas>
          </div>
          <div class="chart-desc">
            Shows which factors are driving up your risk score (e.g. Backlogs, Attendance shortage, or Low Internals).
          </div>
        </div>

        <!-- Graph 2: Student vs Safe Benchmark -->
        <div class="chart-box">
          <div class="chart-title">
            <span>Your Performance vs. Safe Benchmark</span>
            <span style="font-size: 11px; color: #38bdf8; font-weight: 600;">Direct Comparison</span>
          </div>
          <div class="chart-container-fixed">
            <canvas id="benchmarkChart"></canvas>
          </div>
          <div class="chart-desc">
            Compares your attendance, internal test marks, and study score directly against the minimum safe zone.
          </div>
        </div>

      </div>
    </div>

  </div>

  <script>
    let chartBreakdown = null;
    let chartBenchmark = null;

    function toggleAnalytics() {
      const panel = document.getElementById('analyticsPanel');
      if (panel.style.display === 'block') {
        panel.style.display = 'none';
        document.getElementById('btnToggleAnalytics').innerHTML = '<span>📊</span> View Graphs';
      } else {
        panel.style.display = 'block';
        document.getElementById('btnToggleAnalytics').innerHTML = '<span>✕</span> Hide Graphs';
        panel.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function renderCharts(breakdown, metrics) {
      // 1. Risk Contribution Chart
      const ctxBreakdown = document.getElementById('breakdownChart').getContext('2d');
      if (chartBreakdown) chartBreakdown.destroy();
      chartBreakdown = new Chart(ctxBreakdown, {
        type: 'bar',
        data: {
          labels: ['Backlogs', 'Attendance', 'Internals', 'Past SGPA', 'Study/Labs'],
          datasets: [{
            label: 'Risk Contribution Points',
            data: [
              breakdown.backlog_impact,
              breakdown.attendance_impact,
              breakdown.internal_impact,
              breakdown.sgpa_impact,
              breakdown.study_impact
            ],
            backgroundColor: [
              'rgba(239, 68, 68, 0.8)',
              'rgba(245, 158, 11, 0.8)',
              'rgba(59, 130, 246, 0.8)',
              'rgba(168, 85, 247, 0.8)',
              'rgba(16, 185, 129, 0.8)'
            ],
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#9ca3af', font: { size: 10 } } },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af', font: { size: 10 } } }
          }
        }
      });

      // 2. Student vs Safe Benchmark Chart
      const ctxBench = document.getElementById('benchmarkChart').getContext('2d');
      if (chartBenchmark) chartBenchmark.destroy();
      chartBenchmark = new Chart(ctxBench, {
        type: 'bar',
        data: {
          labels: ['Attendance %', 'Internals %', 'SGPA % Equivalent', 'Study Routine %'],
          datasets: [
            {
              label: 'Your Score',
              data: [metrics.attendance, metrics.internals, metrics.prev_sgpa_pct, metrics.study_pct],
              backgroundColor: 'rgba(56, 189, 248, 0.85)',
              borderRadius: 4
            },
            {
              label: 'Safe Threshold',
              data: [75, 50, 60, 50],
              backgroundColor: 'rgba(255, 255, 255, 0.15)',
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { 
            legend: { 
              labels: { color: '#9ca3af', font: { size: 10 }, boxWidth: 10 } 
            } 
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#9ca3af', font: { size: 10 } } },
            y: { 
              grid: { color: 'rgba(255,255,255,0.05)' }, 
              ticks: { color: '#9ca3af', font: { size: 10 }, callback: v => v + '%' },
              max: 100
            }
          }
        }
      });
    }

    function handlePrediction(event) {
      event.preventDefault();
      
      const btn = document.getElementById('btnCheck');
      btn.innerText = 'Calculating...';
      btn.disabled = true;

      const payload = {
        attendance: document.getElementById('attendance').value,
        backlogs: document.getElementById('backlogs').value,
        internals: document.getElementById('internals').value,
        prev_sgpa: document.getElementById('prev_sgpa').value,
        study_hours: document.getElementById('study_hours').value,
        assignments: document.getElementById('assignments').value
      };

      fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(response => response.json())
      .then(data => {
        document.getElementById('placeholderView').style.display = 'none';
        const resView = document.getElementById('resultView');
        resView.style.display = 'block';

        const circle = document.getElementById('riskScoreCircle');
        const badge = document.getElementById('riskBadge');
        const summary = document.getElementById('summaryText');
        const sugg = document.getElementById('suggestionsBox');

        const prob = data.risk_probability;
        circle.innerText = prob + '%';

        if (data.prediction === 'At Risk') {
          circle.className = 'score-circle score-risk';
          badge.className = 'status-badge badge-risk';
          badge.innerText = 'High Risk of Semester Failure / KT';
          summary.innerText = 'Your current profile indicates substantial risk. Low attendance, active backlogs, or weak internal assessment scores are significantly increasing your failure probability.';
          sugg.innerHTML = '<b>Immediate Action Checklist:</b><br>&bull; Keep attendance strictly above 75% to avoid exam detention.<br>&bull; Dedicate 2+ hours daily specifically to clear backlog papers.<br>&bull; Submit all lab manuals and assignments to secure internal grace marks.';
        } else {
          circle.className = 'score-circle score-safe';
          badge.className = 'status-badge badge-safe';
          badge.innerText = 'Safe / Satisfactory Academic Standing';
          summary.innerText = 'Your academic indicators are solid. With consistent study and safe attendance levels, your risk of failing this semester remains minimal.';
          sugg.innerHTML = '<b>Recommendations:</b><br>&bull; Maintain your current attendance and internal test score cadence.<br>&bull; Focus additional study time on high-credit core subjects.';
        }

        document.getElementById('btnToggleAnalytics').style.display = 'inline-flex';
        document.getElementById('analyticsPanel').style.display = 'block';
        document.getElementById('btnToggleAnalytics').innerHTML = '<span>✕</span> Hide Graphs';

        renderCharts(data.breakdown, data.student_metrics);
      })
      .catch(err => {
        alert('Error calculating prediction. Please try again.');
        console.error(err);
      })
      .finally(() => {
        btn.innerText = 'Calculate Academic Risk';
        btn.disabled = false;
      });
    }
  </script>
</body>
</html>"""

class RealAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

    def do_POST(self):
        if self.path == "/predict":
            length = int(self.headers.get("content-length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body)
            result = predict_single(data)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

def run_server(port=8501):
    server = HTTPServer(("127.0.0.1", port), RealAppHandler)
    print("\n" + "=" * 55)
    print(f" Real Academic Risk App LIVE at: http://127.0.0.1:{port}")
    print(" Press Ctrl + C in this window to stop")
    print("=" * 55 + "\n")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
