
const API_URL = "http://127.0.0.1:5000/customers";
const username = "test";
const password = "test@123456";
const authHeader = "Basic " + btoa(`${username}:${password}`);

async function getCustomers() {
  const res = await fetch(API_URL, {
    headers: {
      "Authorization": authHeader
    }
  });
  const customers = await res.json();
  const table = document.getElementById("customerTable");
  table.innerHTML = "";
  customers.forEach(c => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${c.id}</td>
      <td><input value="${c.name}" id="name-${c.id}"></td>
      <td><input value="${c.email}" id="email-${c.id}"></td>
      <td><input value="${c.phone}" id="phone-${c.id}"></td>
      <td>
        <button onclick="updateCustomer(${c.id})">Update</button>
        <button onclick="deleteCustomer(${c.id})">Delete</button>
      </td>
    `;
    table.appendChild(row);
  });
}

async function addCustomer() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const phone = document.getElementById("phone").value;

  await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": authHeader
    },
    body: JSON.stringify({ name, email, phone })
  });

  if(document.getElementById("name").value == ""){
    alert("");
  }
  else{
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("phone").value = "";
  }
  getCustomers();
}

async function deleteCustomer(id) {
  await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": authHeader
    }
  });
  getCustomers();
}

async function updateCustomer(id) {
  const name = document.getElementById(`name-${id}`).value;
  const email = document.getElementById(`email-${id}`).value;
  const phone = document.getElementById(`phone-${id}`).value;

  await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": authHeader
    },
    body: JSON.stringify({ name, email, phone })
  });
  getCustomers();
}

window.onload = getCustomers;
