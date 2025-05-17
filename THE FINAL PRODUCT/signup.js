
const signupForm = document.getElementById('signupForm');
if (signupForm) {
  signupForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;


    if (/\s/.test(password) || password.length < 8) {
      alert('Password cannot contain spaces and must be at least 8 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    const newUser = { name, email, password };
    let customers = JSON.parse(localStorage.getItem('customers')) || [];
    const exists = customers.some(user => user.email === email);

    if (exists) {
      alert('Email already registered!');
      return;
    }

    customers.push(newUser);
    localStorage.setItem('customers', JSON.stringify(customers));
    alert('Customer account created successfully!');
    window.location.href = 'login.html';
  });
}
