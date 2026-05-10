from flask import Flask, render_template_string, redirect, url_for, request, session, flash
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

#(need i-replace ng real db)
users = {}

SHARED_STYLES = '''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f7f7f5;
    --surface: #ffffff;
    --border: #e2e2dc;
    --border-strong: #c8c8c0;
    --accent-a: #185FA5;
    --accent-b: #3B6D11;
    --accent-r: #A32D2D;
    --text: #1a1a1a;
    --muted: #6b6b66;
    --cell-bg: #f0f4fb;
    --cell-focus-border: #378ADD;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: "Space Mono", monospace;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }

  .auth-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 40px 36px 36px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 2px 24px rgba(0,0,0,0.05);
  }

  .logo {
    text-align: center;
    margin-bottom: 28px;
  }
  .logo h1 {
    font-family: "Syne", sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
  }
  .logo h1 span.a { color: var(--accent-a); }
  .logo h1 span.b { color: var(--accent-b); }
  .logo h1 span.r { color: var(--accent-r); }
  .logo p {
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  .tabs {
    display: flex;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 4px;
    margin-bottom: 28px;
    gap: 4px;
  }
  .tab {
    flex: 1;
    padding: 8px;
    text-align: center;
    font-family: "Space Mono", monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--muted);
    text-decoration: none;
    border-radius: var(--radius-sm);
    transition: background 0.15s, color 0.15s;
  }
  .tab:hover { color: var(--text); }
  .tab.active {
    background: var(--accent-a);
    color: #fff;
  }

  .form-group { margin-bottom: 16px; }
  .form-group label {
    display: block;
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
  }
  .form-group input {
    width: 100%;
    height: 42px;
    padding: 0 14px;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    background: var(--cell-bg);
    color: var(--text);
    font-family: "Space Mono", monospace;
    font-size: 0.85rem;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s, background 0.15s;
  }
  .form-group input:hover { background: #fff; }
  .form-group input:focus {
    border-color: var(--cell-focus-border);
    box-shadow: 0 0 0 3px rgba(55,138,221,0.12);
    background: #fff;
  }
  .form-group input.error { border-color: var(--accent-r); }

  .pw-wrap { position: relative; }
  .pw-wrap input { padding-right: 42px; }
  .pw-toggle {
    position: absolute;
    right: 12px; top: 50%;
    transform: translateY(-50%);
    background: none; border: none; cursor: pointer;
    color: var(--muted); padding: 0;
    transition: color 0.15s;
  }
  .pw-toggle:hover { color: var(--text); }
  .pw-toggle svg { width: 16px; height: 16px; display: block; }

  .field-hint {
    font-size: 0.62rem;
    color: var(--muted);
    margin-top: 5px;
    letter-spacing: 0.3px;
  }
  .field-error {
    font-size: 0.62rem;
    color: var(--accent-r);
    margin-top: 5px;
    letter-spacing: 0.3px;
  }

  .alert {
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 0.7rem;
    margin-bottom: 18px;
    line-height: 1.5;
  }
  .alert-error {
    background: #fdf0f0;
    border: 1px solid var(--result-border, #f0c0c0);
    color: var(--accent-r);
  }
  .alert-success {
    background: #f0faf3;
    border: 1px solid #b8dfc4;
    color: var(--accent-b);
  }

  .strength-bar {
    display: flex; gap: 4px; margin-top: 8px;
  }
  .strength-seg {
    flex: 1; height: 3px; border-radius: 99px;
    background: var(--border); transition: background 0.2s;
  }
  .strength-label {
    font-size: 0.6rem; color: var(--muted); margin-top: 4px; text-align: right;
  }

  .divider {
    display: flex; align-items: center; gap: 12px;
    margin: 22px 0; color: var(--muted); font-size: 0.65rem;
  }
  .divider::before, .divider::after {
    content: ''; flex: 1;
    height: 1px; background: var(--border);
  }

  .social-btn {
    width: 100%; height: 40px;
    background: transparent;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    font-family: "Space Mono", monospace;
    font-size: 0.72rem;
    color: var(--text);
    cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 10px;
    transition: background 0.15s, border-color 0.15s;
    margin-bottom: 10px;
    text-decoration: none;
  }
  .social-btn:hover { background: var(--bg); border-color: var(--text); }
  .social-btn svg { width: 16px; height: 16px; flex-shrink: 0; }

  .btn-submit {
    width: 100%; height: 44px;
    background: var(--accent-a); color: #fff;
    border: none; border-radius: 999px;
    font-family: "Space Mono", monospace;
    font-size: 0.8rem; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase;
    cursor: pointer; margin-top: 8px;
    transition: opacity 0.15s, transform 0.1s;
  }
  .btn-submit:hover { opacity: 0.88; transform: translateY(-1px); }
  .btn-submit:active { transform: translateY(0); }

  .auth-footer {
    text-align: center;
    margin-top: 20px;
    font-size: 0.68rem;
    color: var(--muted);
  }
  .auth-footer a { color: var(--accent-a); text-decoration: none; }
  .auth-footer a:hover { text-decoration: underline; }

  .checkbox-row {
    display: flex; align-items: flex-start; gap: 10px;
    margin-bottom: 16px;
  }
  .checkbox-row input[type=checkbox] {
    width: 16px; height: 16px; margin-top: 2px; flex-shrink: 0;
    accent-color: var(--accent-a); cursor: pointer;
  }
  .checkbox-row label {
    font-size: 0.68rem; color: var(--muted); cursor: pointer; line-height: 1.5;
    text-transform: none; letter-spacing: 0;
  }
  .checkbox-row label a { color: var(--accent-a); text-decoration: none; }
  .checkbox-row label a:hover { text-decoration: underline; }

  .forgot-row {
    display: flex; justify-content: flex-end; margin-top: -8px; margin-bottom: 16px;
  }
  .forgot-row a { font-size: 0.65rem; color: var(--muted); text-decoration: none; }
  .forgot-row a:hover { color: var(--accent-a); }
</style>
'''

EYE_OPEN = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'''
EYE_CLOSED = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'''

#Login Page
LOGIN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login — Matrix Calculator</title>
''' + SHARED_STYLES + '''
</head>
<body>
<div class="auth-card">

  <div class="logo">
    <h1><span class="a">Addition</span> Matrix <span class="b">Calculator</span><span class="r"></span></h1>
  </div>

  <div class="tabs">
    <a href="/login" class="tab active">Log In</a>
    <a href="/signup" class="tab">Sign Up</a>
  </div>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endwith %}

  <form method="POST" action="/login">
    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" placeholder="you@email.com"
             value="{{ request.form.get('email', '') }}" required />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <div class="pw-wrap">
        <input type="password" id="password" name="password"
               placeholder="••••••••" required />
        <button type="button" class="pw-toggle" onclick="togglePw('password', this)"
                title="Show/hide password">''' + EYE_OPEN + '''</button>
      </div>
    </div>

    <div class="forgot-row">
      <a href="/forgot">Forgot password?</a>
    </div>

    <button type="submit" class="btn-submit">Log In</button>
  </form>

  <div class="auth-footer">
    Don&rsquo;t have an account? <a href="/signup">Sign up</a>
  </div>

</div>

<script>
function togglePw(id, btn) {
  const inp = document.getElementById(id);
  if (inp.type === 'password') {
    inp.type = 'text';
    btn.innerHTML = "''' + EYE_CLOSED.replace("'", "\\'") + '''";
  } else {
    inp.type = 'password';
    btn.innerHTML = "''' + EYE_OPEN.replace("'", "\\'") + '''";
  }
}
</script>
</body>
</html>'''


#SigUp Page
SIGNUP_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sign Up — Matrix Calculator</title>
''' + SHARED_STYLES + '''
</head>
<body>
<div class="auth-card">

  <div class="logo">
    <h1><span class="a">Addition</span> Matrix <span class="b">Calculator</span><span class="r"></span></h1>
  </div>

  <div class="tabs">
    <a href="/login" class="tab">Log In</a>
    <a href="/signup" class="tab active">Sign Up</a>
  </div>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endwith %}

  <form method="POST" action="/signup" id="signup-form">

    <div style="display:flex; gap:12px;">
      <div class="form-group" style="flex:1;">
        <label for="first_name">First Name</label>
        <input type="text" id="first_name" name="first_name"
               placeholder="John" value="{{ request.form.get('first_name', '') }}" required />
      </div>
      <div class="form-group" style="flex:1;">
        <label for="last_name">Last Name</label>
        <input type="text" id="last_name" name="last_name"
               placeholder="Doe" value="{{ request.form.get('last_name', '') }}" required />
      </div>
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email"
             placeholder="you@email.com" value="{{ request.form.get('email', '') }}" required />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <div class="pw-wrap">
        <input type="password" id="password" name="password"
               placeholder="Min. 8 characters" required oninput="checkStrength(this.value)" />
        <button type="button" class="pw-toggle" onclick="togglePw('password', this)"
                title="Show/hide password">''' + EYE_OPEN + '''</button>
      </div>
      <div class="strength-bar">
        <div class="strength-seg" id="seg1"></div>
        <div class="strength-seg" id="seg2"></div>
        <div class="strength-seg" id="seg3"></div>
        <div class="strength-seg" id="seg4"></div>
      </div>
      <div class="strength-label" id="strength-label">&nbsp;</div>
    </div>

    <div class="form-group">
      <label for="confirm_password">Confirm Password</label>
      <div class="pw-wrap">
        <input type="password" id="confirm_password" name="confirm_password"
               placeholder="Repeat password" required />
        <button type="button" class="pw-toggle" onclick="togglePw('confirm_password', this)"
                title="Show/hide password">''' + EYE_OPEN + '''</button>
      </div>
    </div>

    <div class="checkbox-row">
      <input type="checkbox" id="terms" name="terms" required />
      <label for="terms">
        I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
      </label>
    </div>

    <button type="submit" class="btn-submit">Create Account</button>
  </form>

  <div class="auth-footer">
    Already have an account? <a href="/login">Log in</a>
  </div>

</div>

<script>
function togglePw(id, btn) {
  const inp = document.getElementById(id);
  if (inp.type === 'password') {
    inp.type = 'text';
    btn.innerHTML = "''' + EYE_CLOSED.replace("'", "\\'") + '''";
  } else {
    inp.type = 'password';
    btn.innerHTML = "''' + EYE_CLOSED.replace("'", "\\'") + '''";
  }
}

function checkStrength(val) {
  let score = 0;
  if (val.length >= 8) score++;
  if (/[A-Z]/.test(val)) score++;
  if (/[0-9]/.test(val)) score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;

  const colors = ['', '#E24B4A', '#EF9F27', '#185FA5', '#3B6D11'];
  const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
  for (let i = 1; i <= 4; i++) {
    const seg = document.getElementById('seg' + i);
    seg.style.background = i <= score ? colors[score] : 'var(--border)';
  }
  document.getElementById('strength-label').textContent = val.length ? labels[score] : '';
}
</script>
</body>
</html>'''


#Forgot Password Page
FORGOT_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Forgot Password — Matrix Calculator</title>
''' + SHARED_STYLES + '''
</head>
<body>
<div class="auth-card">

  <div class="logo">
    <h1><span class="a">A</span> + <span class="b">B</span> = <span class="r">R</span></h1>
    <p>Matrix Addition Calculator</p>
  </div>

  <div style="margin-bottom:24px;">
    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:6px;">Reset your password</div>
    <div style="font-size:0.72rem;color:var(--muted);line-height:1.6;">
      Enter your email and we&rsquo;ll send you a reset link if an account exists.
    </div>
  </div>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endwith %}

  <form method="POST" action="/forgot">
    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" placeholder="you@email.com" required />
    </div>
    <button type="submit" class="btn-submit">Send Reset Link</button>
  </form>

  <div class="auth-footer" style="margin-top:16px;">
    <a href="/login">&larr; Back to login</a>
  </div>

</div>
</body>
</html>'''


#Routes
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('calculator'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if email in users and users[email]['password'] == password:
            session['user'] = email
            session['name'] = users[email]['name']
            return redirect(url_for('calculator'))
        flash('Invalid email or password.', 'error')
    return render_template_string(LOGIN_HTML)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first = request.form.get('first_name', '').strip()
        last  = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        pw    = request.form.get('password', '')
        pw2   = request.form.get('confirm_password', '')
        terms = request.form.get('terms')

        if not terms:
            flash('You must agree to the Terms of Service.', 'error')
        elif len(pw) < 8:
            flash('Password must be at least 8 characters.', 'error')
        elif pw != pw2:
            flash('Passwords do not match.', 'error')
        elif email in users:
            flash('An account with that email already exists.', 'error')
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Please enter a valid email address.', 'error')
        else:
            users[email] = {'password': pw, 'name': first + ' ' + last}
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template_string(SIGNUP_HTML)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        flash('If that email exists, a reset link has been sent.', 'success')
    return render_template_string(FORGOT_HTML)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/calculator')
def calculator():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f'''
    <p style="font-family:monospace;padding:40px;text-align:center;">
      Welcome, {session.get("name", "User")}!<br><br>
      <a href="/logout">Log out</a><br><br>
      <small style="color:#888;">In your combined app, render the calculator template here.</small>
    </p>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
