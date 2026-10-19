"""HTML of the login page; Jinja escapes every inserted value."""

LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Přihlášení – Quantum chaos</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <main class="login-page">
    <form class="card login-card" method="post" action="/login">
      <h1>Přihlášení</h1>
      <p class="hint">Výuková a výzkumná aplikace o Monte Carlu a Gaussian Boson Samplingu.</p>
      {% if error %}<p class="error-message" role="alert">{{ error }}</p>{% endif %}
      <input type="hidden" name="next" value="{{ next_path }}">
      <div class="field">
        <label for="user">Uživatel</label>
        <input id="user" name="user" autocomplete="username" required autofocus>
      </div>
      <div class="field">
        <label for="password">Heslo</label>
        <input id="password" name="password" type="password" autocomplete="current-password" required>
      </div>
      <button class="primary-button" type="submit">Přihlásit</button>
    </form>
  </main>
</body>
</html>
"""
