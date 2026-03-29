const RESOURCES = [
  "izvodjac",
  "album",
  "pesma",
  "korisnik",
  "recenzija",
  "zanr",
];

const POLJA = {
  izvodjac: [
    { name: "ime", label: "Ime", type: "text" },
    { name: "zemlja", label: "Zemlja", type: "text" },
    { name: "osnovan", label: "Osnovan", type: "number", step: "1" },
  ],
  album: [
    { name: "naziv", label: "Naziv", type: "text" },
    { name: "godina", label: "Godina", type: "number", step: "1" },
    { name: "izvodjac_id", label: "Izvođač ID", type: "number", step: "1" },
  ],
  pesma: [
    { name: "redni_broj", label: "Redni broj", type: "number", step: "1" },
    { name: "naziv", label: "Naziv", type: "text" },
    { name: "trajanje", label: "Trajanje", type: "number", step: "1" },
    { name: "album_id", label: "Album ID", type: "number", step: "1" },
  ],
  korisnik: [
    { name: "ime", label: "Ime", type: "text" },
    { name: "email", label: "Email", type: "text" },
  ],
  recenzija: [
    { name: "ocena", label: "Ocena", type: "number", step: "1" },
    { name: "komentar", label: "Komentar", type: "text" },
    { name: "album_id", label: "Album ID", type: "number", step: "1" },
    { name: "korisnik_id", label: "Korisnik ID", type: "number", step: "1" },
  ],
  zanr: [{ name: "naziv", label: "Naziv", type: "text" }],
};

const resourceSelect = document.getElementById("resource");
const methodSelect = document.getElementById("method");
const idField = document.getElementById("id-field");
const idInput = document.getElementById("resource-id");
const fieldsField = document.getElementById("fields-field");
const fieldContainer = document.getElementById("field-container");
const form = document.getElementById("request-form");
const output = document.getElementById("output");
const statusEl = document.getElementById("status");
const clearBtn = document.getElementById("clear-output");
const BASE_URL = "/api";

function postaviStatus(text, isError = false) {
  statusEl.textContent = text;
  statusEl.style.color = isError ? "#c9472d" : "#2f7a68";
}

function lepoIspisi(data) {
  if (typeof data === "string") {
    output.textContent = data;
    return;
  }
  output.textContent = JSON.stringify(data, null, 2);
}

async function posaljiZahtev(method, resource, id, body) {
  let url = `${BASE_URL}/${resource}/`;
  if (id && method !== "GET") {
    url = `${BASE_URL}/${resource}/${id}`;
  }

  const options = { method, headers: {} };
  if (body) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const text = await response.text();
  let parsed;
  try {
    parsed = text ? JSON.parse(text) : null;
  } catch (err) {
    parsed = text;
  }

  return { status: response.status, body: parsed };
}

function osveziVidljivostForme() {
  const method = methodSelect.value;
  const needsId = method === "PATCH" || method === "DELETE";
  const needsBody = method === "POST" || method === "PATCH";
  idField.classList.toggle("hidden", !needsId);
  fieldsField.classList.toggle("hidden", !needsBody);
  if (!needsId) {
    idInput.value = "";
  }
  if (!needsBody) {
    fieldContainer.querySelectorAll("input").forEach((input) => {
      input.value = "";
    });
  }
}

function prikaziPolja() {
  const resource = resourceSelect.value;
  const fields = POLJA[resource] || [];
  fieldContainer.innerHTML = "";
  fields.forEach((field) => {
    const label = document.createElement("label");
    label.textContent = field.label;
    const input = document.createElement("input");
    input.type = field.type === "number" ? "number" : "text";
    if (field.type === "number" && field.step) {
      input.step = field.step;
    }
    input.dataset.field = field.name;
    label.appendChild(input);
    fieldContainer.appendChild(label);
  });
}

function uzmiPodatkeIzPolja(method) {
  const resource = resourceSelect.value;
  const fields = POLJA[resource] || [];
  const data = {};
  const missing = [];
  for (const field of fields) {
    const input = fieldContainer.querySelector(
      `[data-field="${field.name}"]`
    );
    if (!input) {
      continue;
    }
    const raw = input.value.trim();
    if (!raw) {
      if (method === "POST") {
        missing.push(field.label);
      }
      continue;
    }
    if (field.type === "number") {
      const num = Number(raw);
      if (Number.isNaN(num)) {
        return { error: `Polje "${field.label}" mora biti broj.` };
      }
      data[field.name] = num;
    } else {
      data[field.name] = raw;
    }
  }
  if (method === "POST" && missing.length) {
    return { error: `Popuni sva polja: ${missing.join(", ")}` };
  }
  if (method === "PATCH" && Object.keys(data).length === 0) {
    return { error: "Unesi bar jedno polje za izmenu." };
  }
  return { data };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const method = methodSelect.value;
  const resource = resourceSelect.value;
  const id = idInput.value.trim();
  let body = null;

  if (method === "PATCH" || method === "DELETE") {
    if (!id) {
      postaviStatus("Unesi ID.", true);
      return;
    }
  }

  if (method === "POST" || method === "PATCH") {
    const result = uzmiPodatkeIzPolja(method);
    if (result.error) {
      postaviStatus(result.error, true);
      return;
    }
    body = result.data;
  }

  postaviStatus(`Šaljem ${method} zahtev...`);
  try {
    const result = await posaljiZahtev(method, resource, id, body);
    postaviStatus(`Gotovo. Status ${result.status}`);
    lepoIspisi(result.body ?? {});
  } catch (err) {
    postaviStatus("Greška pri zahtevu.", true);
    lepoIspisi(String(err));
  }
});

clearBtn.addEventListener("click", () => {
  output.textContent = "{}";
  postaviStatus("Spreman.");
});

methodSelect.addEventListener("change", osveziVidljivostForme);
resourceSelect.addEventListener("change", () => {
  prikaziPolja();
  osveziVidljivostForme();
});

RESOURCES.forEach((resource) => {
  const option = document.createElement("option");
  option.value = resource;
  option.textContent = resource;
  resourceSelect.appendChild(option);
});

prikaziPolja();
osveziVidljivostForme();
