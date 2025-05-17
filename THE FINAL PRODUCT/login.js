const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const email = this.email.value;
    const password = this.password.value;

  
    if (/\s/.test(password) || password.length < 8) {
      alert('Password cannot contain spaces and must be at least 8 characters long.');
      return;
    }


    if (!localStorage.getItem('adminEmail')) {
      localStorage.setItem('adminEmail', 'admin@c202.com');
    }
    if (!localStorage.getItem('adminPassword')) {
      localStorage.setItem('adminPassword', 'superadmin');
    }

    const validEmailADMIN = localStorage.getItem('adminEmail');
    const validPasswordADMIN = localStorage.getItem('adminPassword');

    // Admin login using localStorage
    if (email === validEmailADMIN && password === validPasswordADMIN) {
      localStorage.setItem('loggedIn', 'true');
      localStorage.setItem('userRole', 'admin');
      window.location.href = 'admin/ADMIN_dashboard.html';
      return;
    }

    // Customer login
    const customers = JSON.parse(localStorage.getItem('customers')) || [];
    const customer = customers.find(user => user.email === email && user.password === password);
    if (customer) {
      localStorage.setItem('loggedIn', 'true');
      localStorage.setItem('userRole', 'customer');
      localStorage.setItem('userName', customer.name);
      window.location.href = 'customer/CUSTOMER_dashboard.html';
      return;
    }

    alert('Invalid email or password!');
  });
}
