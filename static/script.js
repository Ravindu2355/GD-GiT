const statusEl = document.getElementById('status');

document.getElementById('uploadForm').onsubmit = async (e) => {
  e.preventDefault();
  const form = Object.fromEntries(new FormData(e.target));
  await fetch('/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(form)
  });
  pollStatus();
};

function api(action) {
  fetch('/' + action).then(() => pollStatus());
}

async function pollStatus() {
  const res = await fetch('/status');
  const json = await res.json();
  statusEl.innerText = JSON.stringify(json, null, 2);
  if (json.running) setTimeout(pollStatus, 5000);
}